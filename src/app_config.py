import os
import dotenv


class AppConfig:
    def __init__(self):
        dotenv.load_dotenv()
        self.connection_string = os.getenv('CONNECTION_STRING')
        self.token_ = os.getenv('TG_TOKEN')
        port = os.getenv('PORT')
        ip = os.getenv('IP')
        self.ip = ip if ip else "0.0.0.0"
        self.port = port if port else 9097
