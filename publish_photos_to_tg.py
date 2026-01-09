import os
import telegram
import time
import random
import argparse
from dotenv import load_dotenv


def get_images(images_folder):
    images = []
    for root, dirs, files in os.walk(images_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                images.append(os.path.join(root, file))
    return images


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    tg_channel = os.getenv('TG_CHANNEL')
    publish_delay_hours = int(os.getenv('PUBLISH_DELAY', 4))
    publish_delay_seconds = publish_delay_hours * 3600    
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
    bot = telegram.Bot(token=tg_token)
    while True:
        images = get_images(images_folder)
        if not images:
            print('В директории нет изображений')
            time.sleep(publish_delay_seconds)
            continue
        random.shuffle(images)
        for image_path in images:
            with open(image_path, 'rb') as photo:
                bot.send_photo(
                    chat_id=tg_channel,
                    photo=photo
                )
            time.sleep(publish_delay_seconds)
