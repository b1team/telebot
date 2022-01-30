from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = ''
    DB_URL: str = ''

    class Config:
        env_file = '.env'


settings = Settings()
