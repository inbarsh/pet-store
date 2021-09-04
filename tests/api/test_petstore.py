import pytest
import allure
from common import utils
from core.petstore_logger import LOGGER


@pytest.mark.usefixtures('test_setup')
@allure.suite('Add new pet route')
class TestAddNewPet:
    @allure.story('find new pet by id')
    def test_find_new_pet_by_id(self):
        with allure.step('add new pet'):
            LOGGER.info('add new pet')
            url = f'{self.data["basic_url"]}{self.data["pet"]}'
            data = self.data["body"]
            category = utils.generate_random_string(4)
            pet_name = utils.generate_random_string(4)
            tag = utils.generate_random_string(4)
            status = utils.generate_random_status()
            response = utils.add_new_pet(url, data, category, pet_name, tag, status)
            assert response.ok, 'response was not ok'
            LOGGER.info(f'response: {response.text}')
            new_pet_id = response.json().get('id')
        with allure.step('find new pet by id'):
            LOGGER.info('find new pet by id')
            url = f'{self.data["basic_url"]}{self.data["id"].format(new_pet_id)}'
            assert utils.find_by_id(url), 'response was not ok'

    @allure.story('new pet was added to inventory')
    def test_new_pet_was_added_to_inventory(self):
        with allure.step('check current inventory'):
            LOGGER.info('check current inventory')
            url = f'{self.data["basic_url"]}{self.data["inventory"]}'
            response = utils.get(url)
            available_inventory_before = response.json().get('available')
        with allure.step('add new pet'):
            LOGGER.info('add new pet')
            url = f'{self.data["basic_url"]}{self.data["pet"]}'
            data = self.data["body"]
            category = utils.generate_random_string(4)
            pet_name = utils.generate_random_string(4)
            tag = utils.generate_random_string(4)
            status = utils.generate_random_status()
            response = utils.add_new_pet(url, data, category, pet_name, tag, status)
            assert response.ok, 'response was not ok'
            LOGGER.info(f'response: {response.text}')
        with allure.step('check inventory was updated'):
            LOGGER.info('check inventory was updated')
            url = f'{self.data["basic_url"]}{self.data["inventory"]}'
            assert utils.added_to_inventory(url, available_inventory_before), 'inventory was not updated as expected'

    @allure.story('find new pet by status')
    def test_find_new_pet_by_status(self):
        with allure.step('add new pet'):
            LOGGER.info('add new pet')
            url = f'{self.data["basic_url"]}{self.data["pet"]}'
            data = self.data["body"]
            category = utils.generate_random_string(4)
            pet_name = utils.generate_random_string(4)
            tag = utils.generate_random_string(4)
            status = utils.generate_random_status()
            response = utils.add_new_pet(url, data, category, pet_name, tag, status)
            assert response.ok, 'response was not ok'
            LOGGER.info(f'response: {response.text}')
            new_pet_id = response.json().get('id')
        with allure.step('find new pet by status'):
            LOGGER.info('find new pet by status')
            url = f'{self.data["basic_url"]}{self.data["status"].format(status)}'
            assert utils.find_by_status_and_id(url, new_pet_id), 'new pet id was not found in the search'
