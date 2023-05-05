from fastapi import FastAPI, HTTPException

from rcr import models
from rcr.encoders import encode
from rcr.storage import storage

app = FastAPI()


@app.post(
    "/commands",
    response_model=models.Status,
    summary="Compute RCR for a list of commands",
)
async def compute_rcr(data_in: models.CommandsIn) -> models.Status:
    storage.clear()  # always clear the storage, so we don't have to worry about old values
    storage.update(encode(data_in.commands))
    return models.Status(status="OK")


@app.get(
    "/rcr/{command}",
    response_model=models.CommandOut,
    summary="Get RCR for a given command",
)
async def get_command_result(command: str) -> models.CommandOut:
    try:
        return models.CommandOut(rcr=storage[command])
    except KeyError:
        raise HTTPException(status_code=404, detail="Command not found") from None
