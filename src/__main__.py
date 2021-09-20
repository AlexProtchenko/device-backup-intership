from src.app import create_app
from src.app_config import AppConfig

config = AppConfig()
app = create_app()

if __name__ == "__main__":
    app.run(host=config.ip, port=config.port)
