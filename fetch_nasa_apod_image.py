import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
from make_api_images import get_image


def get_nasa_apod(nasa_key):
    apod_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': nasa_key,
        'count': 30
        }
    url = f'{apod_url}?{urlencode(params)}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_nasa_apod_images(nasa_key):
    for index, key in enumerate(get_nasa_apod(nasa_key)):
        image_url = key.get('hdurl') or key.get('url')
        get_image(image_url, index)


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_API_KEY']
    try:
        fetch_nasa_apod_images(nasa_key)
    except ValueError as err:
        print(f'Ошибка данных: {err}')
    except requests.exceptions.HTTPError as err:
        print(f'Сетевая ошибка: {err}')
    except Exception as err:
        print(f'Неизвестная ошибка: {err}')
