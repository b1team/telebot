from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = '5268639708:AAEO1b1oS9BlQlIKF7uN3wVy6y9uOF2qass'
    DB_URL: str = ''

    class Config:
        env_file = '.env'


settings = Settings()
