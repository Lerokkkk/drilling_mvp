from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: ClassVar[Path] = Path(__file__).parent.parent.parent
    model_config = SettingsConfigDict(case_sensitive=False, env_file=Path(BASE_DIR, '.env.dev'))
    db_name: str
    db_user: str
    db_password: str
    db_host: str


settings = Settings()
print(settings.model_config)