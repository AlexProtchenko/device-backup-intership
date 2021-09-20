import base64
import random

import requests


def test_backup_create_data(host):
    with open('./tests/utils/pic.jpg', 'rb') as file:
        binary_input = file.read()
    response = requests.request(method='POST',
                                url=f'{host}/api/backups/save',
                                data=binary_input
                                )
    assert response.status_code == 200
    response_get = requests.request(method='GET',
                                    url=f'{host}/api/backups/latest/',
                                    )
    answer = response_get.json()
    assert response.json() == answer
    _id = answer["id"]
    response_get_data = requests.request(method='GET',
                                         url=f'{host}/api/backups/{_id}',
                                         )
    data = base64.b64encode(binary_input).decode("UTF-8")
    assert response_get_data.json() == data


def test_backup_error(host):
    with open('./tests/utils/big.jpg', 'rb') as file:
        binary_input = file.read()
    response = requests.request(method='POST',
                                url=f'{host}/api/backups/save',
                                data=binary_input
                                )
    assert response.status_code == 400
    assert response.json() == {
        'message': 'Not allowed size',
        'statusCode': 400
    }

    with open('./tests/utils/small.jpeg', 'rb') as file:
        binary_input = file.read()
    response = requests.request(method='POST',
                                url=f'{host}/api/backups/save',
                                data=binary_input
                                )
    assert response.status_code == 400
    assert response.json() == {
        'message': 'Not allowed size',
        'statusCode': 400
    }


def test_subs_id(host):
    id_input = {"id": random.randint(1000000, 9999999)}
    response = requests.request(method='POST',
                                url=f'{host}/api/insert-sub',
                                json=id_input
                                )
    assert response.status_code == 200

