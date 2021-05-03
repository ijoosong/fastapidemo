import azure.functions as func
from .http_asgi import AsgiMiddleware
from api_app import app
from typing import Optional
from pydantic import BaseModel
from hashlib import sha1
from json import dumps
from os import getenv
from pathlib import Path
from time import time
from typing import Optional, Dict


from app.griffify import BubbleLetterArt
from app.models import Colour

CACHE = Path(getenv("LOCATION", "./static"))
CACHE.mkdir(exist_ok=True)

def dicthash(data: dict) -> str:
    """Take a dictionary and convert it to a SHA-1 hash."""
    return sha1(dumps(data).encode()).hexdigest()


@app.get("/{letter}")
async def get_griffy(letter: str, options: Optional[Colour] = None) -> Dict[str, str]:
    """Create a new Griff-ify avatar from given letter."""
    if options:
        dh = dicthash(options.dict())
        file = CACHE / f"{dh}.png"

        if not file.exists():
            BubbleLetterArt().generate(letter, options).save(file)
    else:
        dh = sha1(str(time()).encode()).hexdigest()
        file = CACHE / f"{dh}.png"

        BubbleLetterArt().generate(letter).save(file)

    return {"file": f"/static/{dh}.png"}


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)