import random
import string
import requests
from core.petstore_logger import LOGGER
from time import sleep


def post(url, body):
    LOGGER.info(f'url: {url}')
    LOGGER.info(f'data: {body}')
    return requests.post(url, json=body)


def add_new_pet(url, data, category_name, pet_name, tag_name, status):
    data["category"]["name"] = category_name
    data["name"] = pet_name
    data["tags"][0]["name"] = tag_name
    data["status"] = status
    return post(url, data)


def get(url):
    LOGGER.info(f'url: {url}')
    return requests.get(url)


def find_by_id(url):
    for _ in range(5):
        response = get(url)
        if response.ok:
            return True
        sleep(1)
    return False


def find_by_status_and_id(url, pet_id):
    for _ in range(5):
        response = get(url)
        assert response.ok, 'response was not ok'
        for item in response.json():
            if item.get('id') == pet_id:
                return True
        sleep(1)
    return False


def added_to_inventory(url, available_inventory_before):
    for _ in range(5):
        response = get(url)
        assert response.ok, 'response was not ok'
        available_inventory_after = response.json().get('available')
        if available_inventory_after == available_inventory_before + 1:
            return True
        sleep(1)
    LOGGER.info(f'inventory was not updated as expected, the inventory before the addition was '
                f'{available_inventory_before} and now it is {available_inventory_after}')
    return False


def generate_random(size, symbols):
    return ''.join(random.choices(symbols, k=size))


def generate_random_string(size):
    return generate_random(size, string.ascii_lowercase)


def generate_random_status():
    status_list = ['available', 'pending', 'sold']
    return random.choice(status_list)
