import os

from pydantic import Field, BaseModel, AnyHttpUrl, PostgresDsn, BaseSettings


class Settings(BaseSettings):
    ...
    pgurl: PostgresDsn = Field(
        default="postgresql://postgres:postgres@localhost:5432/postgres"
    )
    """Postgres数据库链接信息"""

    api_key: str = ""
    """Bungie API Key"""

    client_secret: str = ""
    """Bungie Client Secret"""

    log_level: str = "INFO"
    """日志级别"""

    upload_url: str = os.environ.get("UPLOAD_URL") or ""

    upload_key: str = os.environ.get("UPLOAD_KEY") or ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


config = Settings()
