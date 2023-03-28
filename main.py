import logging

from service.flickr_service import FlickrService

logging.basicConfig()

LOGGER = logging.getLogger('dataset')
LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    FlickrService().download_images()