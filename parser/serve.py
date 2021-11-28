from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.scraper import urls as s_urls


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


app.include_router(s_urls.router)
