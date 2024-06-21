import logging

from python.learningdeep.examples.example_utils import (
        search_ddg,
        search_images,
        setup_basedir,
        get_photos,
        resize_images,
        verify_photos,
    )

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class DataLoader(object):
    """
    Description: Example class to hold methods for
        downloading images to a directory to provide
        to a trained model from the first exercise in
        the fastai deep learning course.
    """
    def __init__(self, name="ExampleDataLoader"):
        """
        Description: Initialize the class and variables

        Args:
            name (str, optional): name of this class.
                Defaults to "ExampleClassifier."
        """
        self.__name = name

    def __str__(self):
        """
        Description: What to do when you print this class
        """
        logging.info(self.__name)
        return self.__name

    def _get_sample_photos(self, urls):
        """
        Description: Take a random sampling of photos given the URL diets

        Args:
            urls (list): a list of URL dictionaries
        """
        
        self._get_photos('bird', urls)
        self._get_photos('forest', urls)
        

    def _get_photos(self, photo_type, urls, base_path='bird_or_not'):
        """
        Descripton: Given a photo type, perform and download the images

        Args:
            photo_type (str): the type of photo to search, i.e., 'bird'
            urls (list): a list of URL dictionaries
            base_path (str, optional): base path directory name.
                Defaults to 'bird_or_not'.

        Returns:
            path_obj (`fastcore.all`:object): 
        """
        path_obj, dest_obj = setup_basedir(base_path, photo_type)

        get_photos(photo_type, dest_obj)
        get_photos(f"{photo_type} sun photo", dest_obj)
        get_photos(f"{photo_type} shade photo", dest_obj)
        
        resize_images(path_obj/photo_type, max_size=400, dest=path_obj/photo_type)

        return path_obj
    
    def _verify_photos(self, path_obj):
        """
        Description: remove broken/incomplete downloads
        
        Args:

        Returns:
            None
        """
        failed = verify_photos(path_obj)
        if failed:
            logging.info(f"Images that failed to download: {failed}")

    def execute(self):
        """
        Description: Main executing function
        """

        search_ddg("bird photos")
        urls = search_images("bird_photos", max_images=40)
        
        # download a sampling of photos
        path_obj = self._get_sample_photos(urls)

        # remove broken/incomplete downloads
        self._verify(path_obj)
