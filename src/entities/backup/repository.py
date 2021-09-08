from sqlalchemy import MetaData, Table, Column, String, TIMESTAMP, Text
import uuid

from src.entities.backup.model import Backup
from src.sql_config import SqlConfig

BACKUPS: Table


def describe_table(metadata: MetaData) -> Table:
    return Table(
        "backups",
        metadata,
        Column('id', String, primary_key=True),
        Column('binary', Text),
        Column('time', String, nullable=False)
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
        return [row.binary for row in rows]

    def get_latest_time(self):
        statement = BACKUPS.select()
        with self.engine.begin() as connection:
            rows = connection.execute(statement).all()
        return [row.time for row in rows]

    def add(self, backup: Backup):
        statement = BACKUPS.insert().values(
            id=backup.test_id,
            binary=backup.binary,
            time=backup.time
        )
        with self.engine.begin() as connection:
            connection.execute(statement)
