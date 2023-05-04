from typing import Literal, Union, List

from pydantic import BaseModel, ConstrainedStr

from rcr.config import settings


class Status(BaseModel):

    status: Literal["OK"]


class Command(ConstrainedStr):
    def validate(cls, value: Union[str]) -> Union[str]:
        if value not in settings.commands:
            raise ValueError(f"Unknown command '{value}'.")
        return value


class CommandsIn(BaseModel):

    commands: List[Command]


class CommandOut(BaseModel):

    rcr: str
