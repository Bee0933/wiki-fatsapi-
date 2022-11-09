from fastapi import APIRouter, status, HTTPException, Depends
from logic import search_page, search_wiki
from .schema import key_search, page_search
from .auth_routes import AuthJWT

wiki_route = APIRouter(prefix="/wiki", tags=["WIKI"])


# search titles
@wiki_route.post("/search-titles", status_code=status.HTTP_201_CREATED)
async def search_titles(key: key_search, Authorize: AuthJWT = Depends()) -> dict:

    try:
        # request access token from authorized user
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized token"
        ) from e

    try:
        titles = search_wiki(key)
        return {"message": titles}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"unidentified keyword | error -> {e}",
        ) from e


# search pages
@wiki_route.post("/search-pages", status_code=status.HTTP_201_CREATED)
async def search_pages(title: page_search, Authorize: AuthJWT = Depends()) -> dict:

    try:
        # request access token from authorized user
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized token"
        ) from e

    try:
        return search_page(title)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"search title does not exist! | error -> {e}",
        ) from e
