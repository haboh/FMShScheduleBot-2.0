# -*- coding: utf-8 -*-
from telebot import TeleBot
import config
from hashlib import md5
from json import dumps
from json import loads
from os import listdir
from time import sleep


class ListOfHashes:
    def __init__(self, filename):
        self.fileName = filename
        open(filename, 'a').close()
        with open(filename, 'r') as curFile:
            empty = (curFile.read() == '')
        if empty:
            with open(filename, 'a') as curFile:
                curFile.write('[]')

    def in_list(self, hash_of_image):
        with open(self.fileName, 'r') as curFile:
            list_of_hashes_of_images = loads(curFile.read())
            return hash_of_image in list_of_hashes_of_images

    def get_list(self):
        with open(self.fileName, 'r') as curFile:
            list_of_hashes_of_image = loads(curFile.read())
            return list_of_hashes_of_image

    def add_hash(self, hash_of_image):
        list_of_hashes_of_images = self.get_list()
        if hash_of_image not in list_of_hashes_of_images:
            list_of_hashes_of_images.append(hash_of_image)
        json_list_of_names_of_images = dumps(list_of_hashes_of_images)
        with open(self.fileName, 'w') as curFile:
            curFile.write(json_list_of_names_of_images)


def get_list_of_names_of_all_images():
    return listdir(config.DirectoryWithImages)


def get_hash_of_image(path):
    image = open(path, 'rb')
    hash_of_image = md5(image.read()).hexdigest()
    image.close()
    return hash_of_image


def get_names_of_not_posted_images(list_of_hashes):
    list_of_images_for_post = []
    list_of_names_of_all_images = get_list_of_names_of_all_images()
    for name_of_image in list_of_names_of_all_images:
        hash_of_current_image = get_hash_of_image(config.DirectoryWithImages + '\\' + name_of_image)
        if not list_of_hashes.in_list(hash_of_current_image):
            list_of_hashes.add_hash(hash_of_current_image)
            list_of_images_for_post.append(name_of_image)
    return list_of_images_for_post


def main():
    bot = TeleBot(config.BotToken)
    list_of_hashes = ListOfHashes(config.FileWithListOfHashesOfImages)
    while True:
        try:
            list_of_images_for_post = get_names_of_not_posted_images(list_of_hashes)
            for image_name in list_of_images_for_post:
                bot.send_chat_action(config.ChanelId, 'upload_photo')
                path_to_image = config.DirectoryWithImages + '\\' + image_name
                image_for_post = open(path_to_image, 'rb')
                bot.send_photo(config.ChanelId, image_for_post)
                image_for_post.close()
        finally:
            pass
        sleep(60)


if __name__ == '__main__':
    main()
