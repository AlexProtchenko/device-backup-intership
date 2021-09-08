from http import HTTPStatus
from datetime import timezone,datetime
from src.entities.backup.model import Backup
from flask import Blueprint, jsonify, current_app as app, request
import uuid

backup_controller_api = Blueprint('backup_controller_api', __name__)


@backup_controller_api.route('/api/backups', methods=["GET"])
def get_backups():
    obj = app.config.backup_repository.get()
    return jsonify(obj), HTTPStatus.OK


@backup_controller_api.route('/api/backups/save', methods=["POST"])
def post_backup():
    request.method = 'POST'
    payload = request.data
    test_id = str(uuid.uuid4())
    binary = payload
    time = datetime.now(tz=timezone.utc)
    backup = Backup(test_id, str(binary), time)
    obj = app.config.backup_repository.add(backup)
    return '', HTTPStatus.OK
