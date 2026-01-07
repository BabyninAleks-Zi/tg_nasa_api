import os
import requests
import argparse
from make_api_images import get_image


def get_spasex(launch_id=None):
    if launch_id:
        url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    else:
        url = f'https://api.spacexdata.com/v5/launches/latest'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    flickr_images = data['links']['flickr']['original']
    return flickr_images


def fetch_spacex_launch(launch_id=None):
    for index, url in enumerate(get_spasex(launch_id)):
        get_image(url, index)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', help='Введите ID последнего запуска SpaceX')
    args = parser.parse_args()
    try:
        fetch_spacex_launch(args.id)
    except ValueError as err:
            print(f'Ошибка данных: {err}')
    except requests.exceptions.HTTPError as err:
            print(f'Сетевая ошибка: {err}')
    except Exception as err:
            print(f'Неизвестная ошибка: {err}')
