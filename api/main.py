from fastapi import FastAPI
from .wiki_routes import wiki_route
from .auth_routes import auth_route


# app instance
app = FastAPI()

# include roues
app.include_router(wiki_route)
app.include_router(auth_route)
