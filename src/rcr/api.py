from fastapi import FastAPI, HTTPException

from rcr import models
from rcr.storage import storage

app = FastAPI()


@app.post(
    "/commands",
    response_model=models.Status,
    summary="Compute RCR for a list of commands",
)
async def compute_rcr(commands: models.CommandsIn) -> models.Status:
    storage.clear()  # always clear the storage, so we don't have to worry about old values
    storage[commands.commands[0]] = 1
    return {"status": "OK"}


@app.get(
    "/rcr/{command}",
    response_model=models.CommandOut,
    summary="Get RCR for a given command",
)
async def get_command_result(command: str):
    try:
        result = {"rcr": storage[command]}
    except KeyError:
        raise HTTPException(status_code=404, detail="Command not found")
    return result
