from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response

from dotenv import load_dotenv
import os
from pathlib import Path
import tempfile
import shutil

import image

load_dotenv()

TEMP_STORAGE_LOCATION = Path(os.environ.get("TEMP_STORAGE", tempfile.gettempdir()))
IMG_DIRECTORY = TEMP_STORAGE_LOCATION / "img"



def initApplication():
    # Create directories
    IMG_DIRECTORY.mkdir(parents=True, exist_ok=True)

initApplication()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory=IMG_DIRECTORY), name="img")

templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html",
    )


@app.post("/upload")
async def uploadFiles(upload: UploadFile):

    if upload.size is None:
        return {"error": "Cannot compute file size"}

    max_size = 10 * 1000 * 1000   #10MB
    if upload.size > max_size:
        return {"error": "File too large"}


    # Save file
    random_filename = IMG_DIRECTORY / image.randomFilename()

    with random_filename.open("wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)


    response = Response(headers={
        "HX-Redirect": f"/edit/{random_filename.name}"
    })

    return response


@app.get("/edit/{name}", response_class=HTMLResponse)
async def editFile(request: Request, name: str):
    file_location = IMG_DIRECTORY / name

    if not file_location.exists():
        return f"<div>File {name} does not exist.</div>"

    context = {
        "filename": name
    }

    return templates.TemplateResponse(
        request=request, name="editor.html", context=context
    )
