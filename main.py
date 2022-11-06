from fastapi import FastAPI
from api import wiki_route


app = FastAPI()

app.include_router(wiki_route)
