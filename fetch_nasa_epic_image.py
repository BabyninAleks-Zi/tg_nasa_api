import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
from make_api_images import get_image


def get_nasa_epic(nasa_key):
    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': nasa_key,
        }
    url = f'{epic_url}?{urlencode(params)}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_nasa_epic_images(nasa_key):
    for index, item in enumerate(get_nasa_epic(nasa_key)):
        epic_date = item['date'][:10]
        y, m, d = epic_date.split('-')
        image_url = f'https://epic.gsfc.nasa.gov/archive/natural/\
                    {y}/{m}/{d}/png/{item["image"]}.png'
        get_image(image_url, index)


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_API_KEY']
    try:
        fetch_nasa_epic_images(nasa_key)
    except ValueError as err:
        print(f'Ошибка данных: {err}')
    except requests.exceptions.HTTPError as err:
        print(f'Сетевая ошибка: {err}')
    except Exception as err:
        print(f'Неизвестная ошибка: {err}')
