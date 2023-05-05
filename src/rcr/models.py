from typing import Literal

from pydantic import BaseModel


class Status(BaseModel):

    status: Literal["OK"]


class CommandsIn(BaseModel):

    commands: list[str]


class CommandOut(BaseModel):

    rcr: str
