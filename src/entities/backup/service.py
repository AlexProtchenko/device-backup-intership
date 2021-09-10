from src.entities.backup.exception import DataException
from src.entities.backup.model import Backup
from src.entities.backup.repository import BackupsRepository
from src.sql_config import SqlConfig


class BackupService:
    def __init__(self, sql_config: SqlConfig):
        self.backup_repo = BackupsRepository(sql_config)

    def create(self, backup: Backup):

        if 1024 * 1024 < len(backup.binary) or 1024 * 10 > len(backup.binary):
            raise DataException('Not allowed size')
        else:
            self.backup_repo.add(backup)

    def get_data(self):
        return self.backup_repo.get()

    def get_time(self):
        return self.backup_repo.get_latest_time()
