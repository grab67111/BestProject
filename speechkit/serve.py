from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvloop

from app.recognizers import urls as r_urls
from app.ws import urls as ws_urls


uvloop.install()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def ping():
    return {"message": "Hello!"}


app.include_router(r_urls.router)
app.include_router(ws_urls.router)