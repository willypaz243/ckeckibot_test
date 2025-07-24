from pydantic_settings import BaseSettings


class Config(BaseSettings):
    api_key: str = "your_api_key"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_config():
    return Config()
