from http import HTTPStatus

from src.entities.backup.exception import CustomException, NoDataException
from flask import Blueprint, jsonify, current_app as app, request

backup_controller_api = Blueprint('backup_controller_api', __name__)


@backup_controller_api.route('/api/backups/latest/', methods=["GET"])
def get_time_backups():
    obj = app.config.backup_service.get_time()
    return jsonify(obj), HTTPStatus.OK


@backup_controller_api.route('/api/backups/uuid', methods=['GET'])
def get_time_uuid():
    obj = app.config.backup_service.get_all_uuid()
    return jsonify(obj), HTTPStatus.OK


@backup_controller_api.route('/api/backups/<uuid:_uuid>', methods=['GET'])
def get_backup_uuid(_uuid):
    obj = app.config.backup_service.get_backup_uuid(_uuid)
    return jsonify(obj), HTTPStatus.OK


@backup_controller_api.route('/api/backups/save', methods=["POST"])
def post_backup():
    request.method = 'POST'
    binary = request.data
    backup = app.config.backup_service.create(binary)
    return jsonify(backup), HTTPStatus.OK


@backup_controller_api.errorhandler(CustomException)
def handle_exception(e: NoDataException):
    response = {
        'statusCode': e.status_code,
        'message': e.message
    }
    return jsonify(response), e.status_code
