# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
import os
import dotenv


class AppConfig:
    def __init__(self):
        dotenv.load_dotenv()
        self.connection_string = os.getenv('CONNECTION_STRING')
