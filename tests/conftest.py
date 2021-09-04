import pytest
import json
from os.path import sep as sep
from core import config


@pytest.fixture(scope='session')
def data():
    with open(config.HOME_PATH + sep + 'data' + sep + 'test_data.json',
              encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


@pytest.fixture(scope='class')
def test_setup(data, request):
    request.cls.data = data
