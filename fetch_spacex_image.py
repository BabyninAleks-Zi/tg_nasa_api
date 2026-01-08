import os
import requests
import argparse
from make_api_images import get_image


def get_spasex_images_url(launch_id='latest'):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()
    response_data = response.json()
    flickr_images = response_data['links']['flickr']['original']
    if not flickr_images:
        raise ValueError('SpaceX не вернул ссылки на изображения')
    return flickr_images


def fetch_spacex_launch(image_urls):
    for index, url in enumerate(image_urls):
        get_image(url, index)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Получение изображения с запусков SpaceX')
    parser.add_argument('--id', default='latest', help='Введите ID последнего запуска SpaceX')
    args = parser.parse_args()
    image_urls = get_spasex_images_url(args.id)
    fetch_spacex_launch(image_urls)
