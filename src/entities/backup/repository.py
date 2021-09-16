from sqlalchemy import MetaData, Table, Column, String, LargeBinary, desc
import base64

from src.entities.backup.model import Backup
from src.sql_config import SqlConfig

BACKUPS: Table


def describe_table(metadata: MetaData) -> Table:
    return Table(
        "backups",
        metadata,
        Column('id', String(36), primary_key=True),
        Column('binary', LargeBinary),
        Column('time', String(32), nullable=False)
    )


class BackupsRepository:
    def __init__(self, sql_config: SqlConfig):
        global BACKUPS
        BACKUPS = describe_table(sql_config.metadata)
        self.engine = sql_config.engine

    def get_latest_backup(self):
        statement = BACKUPS.select().order_by(desc(BACKUPS.c.time))
        with self.engine.connect() as connection:
            row = connection.execute(statement).first()
            encoded = base64.b64encode(row.binary)
            result = encoded.decode("UTF-8")
        return result

    def get_latest_time(self):
        statement = BACKUPS.select().order_by(desc(BACKUPS.c.time))
        with self.engine.connect() as connection:
            row = connection.execute(statement).first()
        return row.time  # todo json [id: uuid, create time: time]

    def get_uuid(self):
        statement = BACKUPS.select(BACKUPS.c.time)
        with self.engine.connect() as connection:
            rows = connection.execute(statement).all()
            result = []
            for row in rows:
                result.append([row.time, row.id])
        return result

    def get_backup(self, backup_id: str):
        statement = BACKUPS.select().where(BACKUPS.c.id == str(backup_id))
        with self.engine.connect() as connection:
            row = connection.execute(statement).one_or_none()
            encoded = base64.b64encode(row.binary)
            result = encoded.decode("UTF-8")
        return result

    def add(self, backup: Backup):
        statement = BACKUPS.insert().values(
            id=backup.backup_id,
            binary=backup.binary,
            time=backup.time
        )
        with self.engine.begin() as connection:
            connection.execute(statement)
