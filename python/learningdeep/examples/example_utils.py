"""
# Utilities to download images of birds and non-birds

# install libraries with jupyter notebook syntax for kaggle
!pip install -Uqq fastbook
!pip install -Uqq duckduckgo-images-api
!pip install -U fastai duckduckgo_search
"""

import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
from time import sleep


# try except importing the kaggle jupyter notebook modules
try:
    from fastcore.all import L, Path
    from fastai.vision.all import (
        verify_images,
        get_image_files,
        resize_images,
        Image,
    )
    from fastbook import search_images_ddg
    from fastdownload import download_url
    from duckduckgo_search import DDGS
except ModuleNotFoundError as error:
    logging.debug(f"Could not import: {error}")


def setup_basedir(base_path, photo_type):
    """
    Descripton: set up the directory to save the images to

    Args:
        base_path (str): base directory path
        photo_type (str): the type of photo to get

    Returns:
        path_obj (`fastcore.all`:obj): fastcore destnation (base dir) path object
        dest_obj (`fastcore.all`:obj): fastcore destnation (dest dir) path object
    """
    path_obj = Path(base_path)
    dest_obj = (path_obj/photo_type)
    dest_obj.mkdir(exist_ok=True, parents=True)

    return path_obj, dest_obj

def get_photos(photo_type, dest):
    """
    Descripton: set up the directory to save the images to

    Args:
        photo_type (str): the type of photo to get
        dest (`fastcore.all`:object): the fastcore destination (dest dir) path object

    Returns:
        None
    """
    url_dicts = search_images(f'{photo_type} photo')
    download_images(dest, urls=[item['image'] for item in url_dicts])
    sleep(10)  # Pause between searches to avoid over-loading server
    

def verify_photos(path_obj):
    """
    Description: remove broken/incomplete downloads

    Args:
        path_obj (`fastcore.all`:obj): fastcore destnation (base dir) path object

    Returns:
        failed
    """
    failed = verify_images(get_image_files(path_obj))
    failed.map(Path.unlink)
    
    return failed

def resize_images(path, photo_type):
    """
    Description: 
    
    Args:
        path (str): directory path
        photo_type (str): type of photo (sub directory)

    Returns:
        None
    """
    resize_images(path/photo_type, max_size=400, dest=path/photo_type)


def search_ddg(term):
    """
    Description: call to fastbook ddg search images method

    Args:
        term (str): the text to search by

    Returns:
        (list) of search results
    """
    results = search_images_ddg(term)
    return results


def search_images(term, max_images=30):
    """
    Description: search method for images given term filter

    Args:
        term (str): the text to search by
        max_images (int, optional): the max results to return.
            Defaults to 30.

    Returns:
        (list) of URLs to images

    Example Usage:
        #NB: `search_images` depends on duckduckgo.com, which doesn't 
        # always return correct responses.
        #  If you get a JSON error, just try running it again 
        #  (it may take a couple of tries).
        urls = search_images('bird photos', max_images=1)
        logging.info(urls[0])
    """
    logging.info(f"Searching for '{term}'")
    return L(DDGS().images(term))


def download_images(url, types=['bird', 'forest']):
    """
    Description: Download a URL and take a look at it

    Args:
        url (str): address location of image
        types (list, optional): type of image to download.
            Defaults to ['bird', 'forest'].
    """
    for image_type in types:
        dest = image_type
        download_url(url.get('image'), dest, show_progress=False)

        im = Image.open(dest)
        im.to_thumb(256,256)
