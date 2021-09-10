from src.app import create_app
from src.app_config import AppConfig

app_config = AppConfig
app = create_app(app_config)

if __name__ == "__main__":
    app.run()
