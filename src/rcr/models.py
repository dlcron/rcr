from typing import Literal, List

from pydantic import BaseModel


class Status(BaseModel):

    status: Literal["OK"]


class CommandsIn(BaseModel):

    commands: List[str]


class CommandOut(BaseModel):

    rcr: str
