from fastapi import FastAPI
from api import wiki_route, auth_route


# app instance
app = FastAPI()

# include roues
app.include_router(wiki_route)
app.include_router(auth_route)
