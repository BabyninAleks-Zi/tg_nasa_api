import os
import requests
from urllib.parse import urlparse, unquote


def get_image(url, index):
    if not url.startswith('http'):
        raise ValueError('Недопустимое URL изображения')
    images_dir = 'images'
    os.makedirs(images_dir, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    filename = f'space_{index}.jpg'
    with open(f'images/{filename}', 'wb') as file:
        file.write(response.content)
    return filename
