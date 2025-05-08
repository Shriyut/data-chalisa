import json
import requests
from typing import List
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from google.auth.transport.requests import Request
from google.oauth2 import id_token

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/name")
def read_root(name: str = Query(default="World", description="Name to greet")):
    return {"message": f"Hello, {name}!"}


@app.get("/names")
def read_name(
        name: str = Query(default="World", description="Name to greet"),
        nicknames: List[str] = Query(default=[], description="List of nicknames")
):
    return {"message": f"Hello, {name}!", "nicknames": nicknames}


# @app.get("/sentences")
# def read_sentences(sentences: List[str] = Query(default=[], description="List of sentences")):
#     return {"sentences": sentences}


# from pydantic import BaseModel
# class SentencesRequest(BaseModel):
#     sentences: List[str]
#
# @app.post("/sentences")
# def read_sentences(request: SentencesRequest):
#     return {"sentences": request.sentences}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


DEIDENTIFY_REQUEST_FILE = "/app/deidentify-request.json" # path insdie docker image
DLP_DEIDENTIFY_API_URL = "https://dlp.googleapis.com/v2/projects/us-gcp-ame-con-ff12d-npd-1/content:deidentify"
REIDENTIFY_REQUEST_FILE = "/app/reidentify-request.json"
DLP_REIDENTIFY_API_URL = "https://dlp.googleapis.com/v2/projects/us-gcp-ame-con-ff12d-npd-1/content:reidentify"


def get_access_token():
    from google.auth import default
    credentials, _ = default()
    credentials.refresh(Request())
    return credentials.token


@app.post("/deidentify")
def deidentify_data():
    try:

        with open(DEIDENTIFY_REQUEST_FILE, 'r') as file:
            deidentify_request = json.load(file)

        access_token = get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(DLP_DEIDENTIFY_API_URL, headers=headers, json=deidentify_request)

        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            return JSONResponse(content={"error": response.text}, status_code=response.status_code)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/reidentify")
def reidentify_data():
    try:

        with open(REIDENTIFY_REQUEST_FILE, 'r') as file:
            reidentify_request = json.load(file)
        access_token = get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(DLP_REIDENTIFY_API_URL, headers=headers, json=reidentify_request)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            return JSONResponse(content={"error": response.text}, status_code=response.status_code)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/masking-test")
def mask_data():
    pass

