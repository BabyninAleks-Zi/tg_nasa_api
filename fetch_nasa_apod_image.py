import os
import requests
from dotenv import load_dotenv
from make_api_images import get_image


def get_nasa_apod(nasa_key):
    apod_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': nasa_key,
        'count': 30
    }
    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    return response.json()


def fetch_nasa_apod_images(apod_items):
    for index, item in enumerate(apod_items):
        image_url = item.get('hdurl') or item.get('url')
        if not image_url:
            raise KeyError('NASA APOD не вернул ссылку на изображение')
        get_image(image_url, index)


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.getenv('NASA_API_KEY')
    if not nasa_key:
        raise ValueError('NASA_API_KEY не задан')
    apod_items = get_nasa_apod(nasa_key)
    fetch_nasa_apod_images(apod_items)
