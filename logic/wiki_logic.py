import wikipedia as wiki


def search_wiki(keyword: str) -> list:
    """
    This is the first test summary, just go through the documentation

    Args:
        keyword (str): input string keyword to return list of titles to be searched on wikipedia plaform

    Returns:
        list: list of available search titles
    """
    return wiki.search(keyword)


def search_page(title: str) -> dict:
    """get relevant informtio about search keyword

    Args:
        title (str): input search title from existing titles

    Returns:
        dict: details in json format
    """
    search_obj = wiki.page(title)
    res_title = search_obj.title
    res_url = search_obj.url
    res_content = search_obj.content
    res_links = search_obj.links

    return {
        "title": res_title,
        "url": res_url,
        "content": res_content,
        "links": res_links,
    }
