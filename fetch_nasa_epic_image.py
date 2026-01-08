import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from make_api_images import get_image


def get_nasa_epic(nasa_key):
    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    if not nasa_key:
        raise ValueError('NASA_API_KEY не задан')
    params = {
        'api_key': nasa_key,
    }
    response = requests.get(epic_url, params=params)
    response.raise_for_status()
    return response.json()


def fetch_nasa_epic_images(nasa_epic_items):
    for index, item in enumerate(nasa_epic_items):
        epic_date = datetime.fromisoformat(item['date'])
        date_path = epic_date.strftime('%Y/%m/%d')
        image_url = f'https://epic.gsfc.nasa.gov/archive/natural/{date_path}/png/{item["image"]}.png'
        get_image(image_url, index)


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_API_KEY']
    nasa_epic_items = get_nasa_epic(nasa_key)
    fetch_nasa_epic_images(nasa_epic_items)
