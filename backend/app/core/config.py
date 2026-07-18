from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Narra API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Backend API for the Narra premium resale marketplace."
    )

    class Config:
        env_file = ".env"


settings = Settings()