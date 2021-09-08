from src.entities.backup.model import Backup
from src.entities.backup.repository import BackupsRepository
from src.sql_config import SqlConfig


class BackupService:
    def __init__(self, sql_config: SqlConfig):
        self.backup_repo = BackupsRepository(sql_config)

    def create(self, backup: Backup):
        self.backup_repo.add(backup)
