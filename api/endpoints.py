from fastapi import APIRouter, status, HTTPException
from logic import search_page, search_wiki

wiki_route = APIRouter(prefix="/wiki", tags=["WIKI"])

# search titles
@wiki_route.post("/search-titles", status_code=status.HTTP_201_CREATED)
async def search_titles(key: str) -> dict:
    try:
        titles = search_wiki(key)
        return {"message": titles}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"unidentified keyword | error -> {e}",
        ) from e


# search titles
@wiki_route.post("/search-pages", status_code=status.HTTP_201_CREATED)
async def search_pages(title: str) -> dict:
    try:
        return search_page(title)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"search title does not exist! | error -> {e}",
        ) from e
