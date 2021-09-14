import base64

import requests


def test_backup_create_data():
    with open('./tests/utils/pic.jpg', 'rb') as file:
        binary_input = file.read()
    response = requests.request(method='POST',
                                url='http://127.0.0.1:5000/api/backups/save',
                                data=binary_input
                                )  # todo dotenv
    assert response.status_code == 200

    response = requests.request(
        method='GET',
        url='http://127.0.0.1:5000/api/backups/'
    )
    assert response.status_code == 200
    assert base64.b64encode(binary_input) == response.text
