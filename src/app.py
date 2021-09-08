from flask import Flask

from src.entities.backup.repository import BackupsRepository
from src.entities.backup.service import BackupService
from src.sql_config import SqlConfig
from src.entities.backup.controller import backup_controller_api


def create_app(connection: str) -> Flask:
    app = Flask(__name__)
    sql_config = SqlConfig(connection)
    app.register_blueprint(backup_controller_api)
    app.config.backup_service = BackupService(sql_config)
    sql_config.metadata.create_all(checkfirst=True)
    return app
#