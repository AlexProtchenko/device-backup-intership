from sqlalchemy import MetaData, Table, Column, String, LargeBinary, desc, Integer
import base64

from src.entities.backup.model import Backup
from src.sql_config import SqlConfig

BACKUPS: Table
SUBS: Table


def describe_table(metadata: MetaData) -> Table:
    return Table(
        "backups",
        metadata,
        Column('id', String(36), primary_key=True),
        Column('binary', LargeBinary),
        Column('time', String(32), nullable=False)
    )


def describe_subs_table(metadata: MetaData) -> Table:
    return Table(
        "subs",
        metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('chat_id', Integer, unique=True)
    )


class BackupsRepository:
    def __init__(self, sql_config: SqlConfig) -> None:
        global BACKUPS
        global SUBS
        SUBS = describe_subs_table(sql_config.metadata)
        BACKUPS = describe_table(sql_config.metadata)
        self.engine = sql_config.engine

    def insert_subs_id(self, sub_id: int) -> None:
        statement = SUBS.insert().values(
            chat_id=sub_id
        )
        with self.engine.begin() as connection:
            connection.execute(statement)

    def select_all_id(self) -> list[str]:
        statement = SUBS.select(SUBS.c.chat_id)
        with self.engine.connect() as connection:
            rows = connection.execute(statement).all()
        return [row.chat_id for row in rows]

    def get_latest_time(self) -> dict:
        statement = BACKUPS.select().order_by(desc(BACKUPS.c.time))
        with self.engine.connect() as connection:
            row = connection.execute(statement).first()
        return {"id": row.id, "createTime": row.time}

    def get_uuid(self) -> list[dict]:
        statement = BACKUPS.select(BACKUPS.c.time)
        with self.engine.connect() as connection:
            rows = connection.execute(statement).all()
            result = []
            for row in rows:
                result.append({"createTme": row.time, "id": row.id})
        return result

    def get_backup(self, backup_id: str) -> str:
        statement = BACKUPS.select().where(BACKUPS.c.id == str(backup_id))
        with self.engine.connect() as connection:
            row = connection.execute(statement).one_or_none()
            encoded = base64.b64encode(row.binary)
            result = encoded.decode("UTF-8")
        return result

    def add(self, backup: Backup) -> None:
        statement = BACKUPS.insert().values(
            id=backup.backup_id,
            binary=backup.binary,
            time=backup.time
        )
        with self.engine.begin() as connection:
            connection.execute(statement)
