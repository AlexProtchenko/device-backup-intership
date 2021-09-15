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
        url='http://127.0.0.1:5000/api/backups/latest'
    )
    assert response.status_code == 200
    code = str(base64.b64encode(binary_input))
    code2 = response.text
    assert code[2:-1] == code2[3:-3]


def test_backup_error():
    with open('./tests/utils/big.jpg', 'rb') as file:
        binary_input = file.read()
    response = requests.request(method='POST',
                                url='http://127.0.0.1:5000/api/backups/save',
                                data=binary_input
                                )
    assert response.status_code == 400
    assert response.json() == {'message': 'Not allowed size', 'statusCode': 400}

    with open('./tests/utils/small.jpeg', 'rb') as file:
        binary_input = file.read()
    response = requests.request(method='POST',
                                url='http://127.0.0.1:5000/api/backups/save',
                                data=binary_input
                                )
    assert response.status_code == 400
    assert response.json() == {'message': 'Not allowed size', 'statusCode': 400}