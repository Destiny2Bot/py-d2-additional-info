from pydantic import (
    BaseModel,
    BaseSettings,
    PostgresDsn,
    AnyHttpUrl,
    Field,
)


class Settings(BaseSettings):
    ...
    pgurl: PostgresDsn = Field(default="postgresql://postgres:postgres@localhost:5432/postgres")
    api_key: str = ''
    client_secret: str = ''
    log_level:str  = 'INFO'


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = "allow"

config = Settings()
