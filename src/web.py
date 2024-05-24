from typing import Annotated, Union

from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="src/html")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html",
    )


StrInput = Annotated[str, Form()]


@app.post("/upload")
async def uploadFiles(link: Union[StrInput, None] = None, upload: Union[UploadFile, None] = None):

    if link is None and upload is None:
        return {"error": "No files provided"}

    if link:
        return {"message": f"URL provided: {link}"}

    return {"message": f"File uploaded: {upload.filename}"}
