from contextlib import suppress
from typing import List, Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):

    commands_path: str
    commands: Optional[List[str]] = None

    class Config:
        env_file = ".env"

    @validator("commands")
    def compute_commands(cls, _v, values, **kwargs) -> List[str]:
        with suppress(FileNotFoundError):
            with open(values["commands_path"], "r") as f:
                return [command.strip() for command in f if command.strip()]
        # emit a warning here
        return []


settings = Settings()
