import datetime


class Backup:
    def __init__(self, backup_id: str, binary: bin, time: datetime.datetime):
        self.backup_id = backup_id
        self.binary = binary
        self.time = time

