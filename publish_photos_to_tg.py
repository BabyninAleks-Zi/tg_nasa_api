import os
import telegram
import time
import random
import argparse
from dotenv import load_dotenv

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL = os.getenv('TG_CHANNEL')
PUBLISH_DELAY_HOURS = int(os.getenv('PUBLISH_DELAY', 4))
PUBLISH_DELAY_SECONDS = PUBLISH_DELAY_HOURS * 3600


def get_images(images_folder):
    images = []
    for root, dirs, files in os.walk(images_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                images.append(os.path.join(root, file))
    return images


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Публикация фотографий в Telegram-канал'
    )
    parser.add_argument(
        '--images-folder',
        help='Путь к папке с изображениями',
        default='images'
    )
    args = parser.parse_args()
    images_folder = args.images_folder
    bot = telegram.Bot(token=TG_TOKEN)
    while True:
        images = get_images(images_folder)
        if not images:
            print('В директории нет изображений')
            time.sleep(PUBLISH_DELAY_SECONDS)
            continue
        random.shuffle(images)
        for image_path in images:
            with open(image_path, 'rb') as photo:
                bot.send_photo(
                    chat_id=TG_CHANNEL,
                    photo=photo
                )
            time.sleep(PUBLISH_DELAY_SECONDS)
