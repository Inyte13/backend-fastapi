from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env')
  salt_rounds: int = 10
  port: int = 3000
  jwt_secret: str
  production: bool = False
  access_token_duration_minutes: int
settings = Settings()  # type: ignore
