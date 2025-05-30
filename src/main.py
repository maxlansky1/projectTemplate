# src/main.py

from configs.config import config

def main():
    print(f"Starting {config.APP_NAME} in {config.ENV} mode")
    print(f"Debug mode is {'on' if config.DEBUG else 'off'}")
    print(f"Server will run on port {config.PORT}")

if __name__ == "__main__":
    main()
