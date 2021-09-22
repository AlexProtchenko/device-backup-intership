import uuid
from datetime import datetime, timezone
from threading import Thread

import requests

from src.entities.backup.exception import DataException, BadRequestException
from src.entities.backup.model import Backup
from src.entities.backup.repository import BackupsRepository
from src.sql_config import SqlConfig


class BackupService:
    def __init__(self, sql_config: SqlConfig, token: str):
        self.backup_repo = BackupsRepository(sql_config)
        self._token = token

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
        result = {"id": backup.backup_id, "createTime": str(backup.time)}
        Thread(target=self.notify_subs, args=[result]).start()
        return result

    def get_time(self):
        return self.backup_repo.get_latest_time()

    def get_all_uuid(self):
        return self.backup_repo.get_uuid()

    def get_backup_uuid(self, _uuid):
        return self.backup_repo.get_backup(_uuid)

    def notify_subs(self, payload: dict):
        ids = self.backup_repo.select_all_id()
        text = f"New backup!\nId: {payload['id']}\nCreate time: {payload['createTime']}"
        for chat_id in ids:
            url_ = f'https://api.telegram.org/bot{self._token}/sendMessage?chat_id={chat_id}&text={text}'
            requests.request(
                method="POST",
                url=url_
            )

    def add_id(self, _id):
        try:
            return self.backup_repo.insert_subs_id(_id)
        except Exception:
            raise BadRequestException('Chat id exist')
