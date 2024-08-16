from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_TITLE: str

    # FastAPI
    FAST_API_PORT: str
    FAST_API_PREFIX: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    @property
    def db_url(self):
        return f"{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
