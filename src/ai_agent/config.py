import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        self.openai_model = os.environ["OPENAI_MODEL"]


settings = Settings()
