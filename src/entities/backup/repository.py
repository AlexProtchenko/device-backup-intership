from sqlalchemy import MetaData, Table, Column, String, LargeBinary
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

    def get(self):
        statement = BACKUPS.select()
        with self.engine.begin() as connection:
            rows = connection.execute(statement).all()
            data_list = [base64.b64encode(row.binary) for row in rows]
        return data_list[-1]

    def get_latest_time(self):
        statement = BACKUPS.select()
        with self.engine.begin() as connection:
            rows = connection.execute(statement).all()
            time_list = [row.time for row in rows]
        return time_list[-1]

    def add(self, backup: Backup):
        statement = BACKUPS.insert().values(
            id=backup.test_id,
            binary=backup.binary,
            time=backup.time
        )
        with self.engine.begin() as connection:
            connection.execute(statement)
