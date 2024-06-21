# download images of birds and non-birds
!pip install -Uqq fastbook
!pip install -Uqq duckduckgo-images-api
!pip install -U fastai duckduckgo_search


# install libraries
from fastbook import search_images_ddg
from fastcore.all import *
from duckduckgo_search import DDGS


def search_ddg(term):
    """
    Description: example method using ddg search images method

    Args:
        term (str): the text to search by

    Returns:
        (list) of search results
    """
    results = search_images_ddg("bird photos")
    return results


def search_images(term, max_images=30):
    """
    Description: search method

    Args:
        term (str): the text to search by
        max_images (Optional:int): the max results to return

    Returns:
        (list) of images
    """
    print(f"Searching for '{term}'")
    return L(DDGS().images(term))

