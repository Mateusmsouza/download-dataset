import os
import urllib.request
import flickrapi

# Set up the Flickr API key and secret
api_key = os.getenv('FLICKR_API_KEY')
api_secret = os.getenv('FLICKR_SECRET')

def download_image_by_id(photo_id: str, save_on_dir: str) -> str:
    # Set up the Flickr API client
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    # Get the URL of the photo with the given ID
    photo_info = flickr.photos.getInfo(photo_id=photo_id)
    caption = photo_info['photo']['description']['_content']
    # Set the path where you want to save the downloaded image
    save_path = f'{save_on_dir}'

    sizes = flickr.photos.getSizes(photo_id=photo_id)['sizes']['size']
    medium_size = next((size for size in sizes if size['label'] == 'Medium'), None)
    large_size = next((size for size in sizes if size['label'] == 'Large'), None)
    
    medium_size_url = medium_size['source']
    medium_large_size = large_size['source']

    # Create the save path directory if it does not exist
    image_dir = f'{save_path}/{photo_id}'
    os.makedirs(image_dir, exist_ok=True)

    # Download images    
    urllib.request.urlretrieve(medium_size_url, os.path.join(image_dir, f'{photo_id}_medium.jpg'))
    urllib.request.urlretrieve(medium_large_size, os.path.join(image_dir, f'{photo_id}_large.jpg'))
    return caption
