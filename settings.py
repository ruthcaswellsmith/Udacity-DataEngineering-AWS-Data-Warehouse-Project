from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_KEY_ID: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    CLUSTER: Optional[str] = ""
    HOST: Optional[str] = ""
    DB_NAME: Optional[str] = ""
    DB_USER: Optional[str] = ""
    DB_PASSWORD: Optional[str] = ""
    DB_PORT: Optional[int] = None
    IAM_ROLE_ARN: Optional[str] = ""
    SECURITY_GROUP_ID: Optional[str] = ""
    LOG_DATA_PATH: Optional[str] = ""
    SONG_DATA_PATH: Optional[str] = ""
    LOG_JSON_PATH: Optional[str] = ""

    class Config:
        case_sensitive: True


config = Settings()
