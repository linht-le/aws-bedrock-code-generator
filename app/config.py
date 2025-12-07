from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # AWS Configuration
    AWS_REGION: str = "ap-northeast-1"
    MODEL_ID: str = "us.amazon.nova-pro-v1:0"

    # AWS Credentials
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()


def get_settings() -> Settings:
    return settings
