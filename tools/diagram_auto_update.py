import subprocess
from pathlib import Path

SRC_DIR = Path(__file__).parent.parent / "src"
DIAGRAMS_DIR = Path(__file__).parent.parent / "diagrams"
OUTPUT_FILE = DIAGRAMS_DIR / "temp_containers.puml"

# Настройка типов и спрайтов по расширению
EXT_SETTINGS = {
    ".py":     ("Python", "python", "code"),
    ".js":     ("JavaScript", "javascript", "code"),
    ".ts":     ("TypeScript", "typescript", "code"),
    ".json":   ("JSON", "json", "config"),
    ".yaml":   ("YAML", "yaml", "config"),
    ".yml":    ("YAML", "yaml", "config"),
    ".txt":    ("Text", "text", "docs"),
    ".md":     ("Markdown", "markdown", "docs"),
    ".ipynb":  ("Notebook", "jupyter", "notebook"),
    ".html":   ("HTML", "html", "web"),
    ".css":    ("CSS", "css", "web"),
}


def get_changed_files():
    result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        stdout=subprocess.PIPE, text=True
    )
    return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]



def build_container_definitions(added_files):
    defines = []
    boundaries = {}

    for filepath in added_files:
        path = Path(filepath)
        if not filepath.startswith("src/") or not path.exists():
            continue

        if path.name == "__init__.py":
            continue

        ext = path.suffix.lower()
        file_type, sprite, tag = EXT_SETTINGS.get(ext, ("File", "file", "other"))

        path = path.resolve()
        rel_path = path.relative_to(SRC_DIR.parent.resolve())

        parts = rel_path.parts  # например: ('src', 'handlers', 'admin.py')

        var_name = (path.stem + "_" + ext.lstrip(".")).lower()
        var_const = var_name.upper()
        vscode_link = f"vscode://file/C:/gleb/projects/projectTemplate/{rel_path.as_posix()}"
        defines.append(f'!define {var_const} "{vscode_link}"')

        current = boundaries
        for part in parts[1:-1]:  # пропускаем 'src', проходим по папкам
            current = current.setdefault(part, {})
        current.setdefault("files", []).append(
            (parts[-1], var_name, file_type, sprite, tag, var_const)
        )

    return defines, boundaries


def write_container_block(f, name, content, indent=0):
    space = " " * indent
    if "files" in content:
        for filename, var_name, file_type, sprite, tag, var_const in content["files"]:
            f.write(f'{space}    Container({var_name}, "{filename}", "{file_type}", "TODO", $tags="{tag}", $sprite="{sprite}", $link={var_const})\n')
    for subfolder, subcontent in content.items():
        if subfolder == "files":
            continue
        f.write(f'{space}    Container_Boundary({subfolder}, "{subfolder}", $tags="code") {{\n')
        write_container_block(f, subfolder, subcontent, indent + 4)
        f.write(f'{space}    }}\n')


def write_temp_puml(defines, boundaries):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in defines:
            f.write(line + "\n")

        f.write("\nContainer_Boundary(src, \"src (исходный код)\", $tags=\"code\") {\n")
        write_container_block(f, "src", boundaries, indent=4)
        f.write("}\n")



if __name__ == "__main__":
    added_files = get_changed_files()
    defines, boundaries = build_container_definitions(added_files)
    write_temp_puml(defines, boundaries)
