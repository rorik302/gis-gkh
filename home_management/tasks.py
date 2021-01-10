import json

from home_management.models import House
from home_management.parsers import PassportParser, AddressParser


def get_passport_info(url):
    parser = PassportParser(url)
    passport_info = parser.get_passport_info()
    return passport_info


def get_passport_url(data):
    parser = AddressParser(data)
    url = parser.get_passport_url()
    return url


def get_and_save_passport_url(fias_id, data):
    url = get_passport_url(data)
    house = House.objects.get(fias_id=fias_id)
    house.passport_url = url
    house.save()
    return url


def get_and_save_passport_info(fias_id, url):
    passport_info = json.dumps(get_passport_info(url), ensure_ascii=False)
    house = House.objects.get(fias_id=fias_id)
    house.passport_info = passport_info
    house.save()
    return passport_info


def get_and_save_passport_url_and_info(fias_id, data):
    url = get_and_save_passport_url(fias_id, data)
    get_and_save_passport_info(fias_id, url)
