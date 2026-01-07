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


def get_extension():
    url = "https://example.com/txt/hello%20world.txt?v=9#python"
    path = urlparse(url).path
    path = unquote(path)
    root, ext = os.path.splitext(path)
    return ext
