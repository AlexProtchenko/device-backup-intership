import uuid
from datetime import datetime, timezone

from src.entities.backup.exception import DataException
from src.entities.backup.model import Backup
from src.entities.backup.repository import BackupsRepository
from src.sql_config import SqlConfig


class BackupService:
    def __init__(self, sql_config: SqlConfig):
        self.backup_repo = BackupsRepository(sql_config)

    def create(self, binary: bytes):
        backup = Backup(
            backup_id=str(uuid.uuid4()),
            binary=binary,
            time=datetime.now(tz=timezone.utc)
        )

        if 1024 * 1024 < len(backup.binary) or 1024 * 10 > len(backup.binary):
            raise DataException('Not allowed size')
        else:
            self.backup_repo.add(backup)

        return {"id": backup.backup_id, "createTime": str(backup.time)}

    def get_time(self):
        return self.backup_repo.get_latest_time()

    def get_all_uuid(self):
        return self.backup_repo.get_uuid()

    def get_backup_uuid(self, _uuid):
        return self.backup_repo.get_backup(_uuid)
