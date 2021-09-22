# Backup WebAPI

Project description 

API for storing your backups

It can save from 10kb to 1mb of space


Install repository:

```pip install poetry```

```poetry install && poetry shell```


Run server (by gunicorn):

```gunicorn -w 2 -b 0.0.0.0:8080 'src.app:create_app()'```


You can use it by Docker

```/api/latest``` return model of the latest backup {id: UUID, createTime: datetime}

```/api/backups/uuid``` return list of all models of the backups {id: UUID, createTime: datetime}

```/api/backups/<uuid>``` return model of the backup by uuid{id: UUID, createTime: datetime}

```/api/backups/save``` save backup
