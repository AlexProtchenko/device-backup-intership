from flask import Flask

from src.app_config import AppConfig
from src.entities.backup.service import BackupService
from src.sql_config import SqlConfig
from src.entities.backup.controller import backup_controller_api


def create_app() -> Flask:
    config = AppConfig()
    app = Flask(__name__)
    sql_config = SqlConfig(config.connection_string)
    app.register_blueprint(backup_controller_api)
    app.config.backup_service = BackupService(sql_config, config.token_)
    sql_config.metadata.create_all(checkfirst=True)
    return app
