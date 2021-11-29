from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependecies import elastic

from app.scraper import urls as s_urls
from app.db import urls as db_urls


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

@app.on_event("shutdown")
async def app_shutdown():
    await elastic.close()


app.include_router(s_urls.router)
app.include_router(db_urls.router)
