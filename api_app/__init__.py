import fastapi
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from os import getenv

CACHE = Path(getenv("LOCATION", "./static"))
CACHE.mkdir(exist_ok=True)

app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory=CACHE), name="static")
