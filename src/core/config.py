from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env')
  salt_rounds: int = 10
  port: int = 3000


settings = Settings()  # type: ignore
