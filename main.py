import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote, urlencode


def get_image(url, index):
    if not url.startswith('http'):
        raise ValueError('Недопустимое URL изображения')
    images_dir = 'images'
    os.makedirs(images_dir, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    filename = f'spaсe_{index}.jpg'
    with open(f'images/{filename}', 'wb') as file:
        file.write(response.content)
    return filename


def get_spasex():
    id = '5eb87d47ffd86e000604b38a'
    url = f'https://api.spacexdata.com/v5/launches/{id}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    flickr_images = data['links']['flickr']['original']
    return flickr_images


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


def get_nasa_epic(nasa_key):
    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': nasa_key,
        }
    url = f'{epic_url}?{urlencode(params)}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_extension():
    url = "https://example.com/txt/hello%20world.txt?v=9#python"
    path = urlparse(url).path
    path = unquote(path)
    root, ext = os.path.splitext(path)
    return ext


def fetch_spacex_last_launch():
    for index, url in enumerate(get_spasex()):
        get_image(url, index)


def fetch_nasa_apod_images(nasa_key):
    for index, key in enumerate(get_nasa_apod(nasa_key)):
        image_url = key.get('hdurl') or key.get('url')
        get_image(image_url, index)


def fetch_nasa_epic_images(nasa_key):
    for index, item in enumerate(get_nasa_epic(nasa_key)):
        epic_date = item['date'][:10]
        y, m, d = epic_date.split('-')
        image_url = f'https://epic.gsfc.nasa.gov/archive/natural/\
                    {y}/{m}/{d}/png/{item["image"]}.png'
        get_image(image_url, index)


def main():
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


if __name__ == '__main__':
    main()
