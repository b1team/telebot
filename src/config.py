from pydantic import BaseSettings


# Thay may cai nayf trong .env -> Doc readme.md
class Settings(BaseSettings):
    BOT_TOKEN: str = ''
    DB_URL: str = ''
    DRIVER_PATH: str = ''

    class Config:
        env_file = '.env'


settings = Settings()
