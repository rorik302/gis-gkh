import json

from home_management.models import House
from home_management.parsers import PassportParser, AddressParser


def get_passport_info(url):
    return PassportParser(url).get_passport_info()


def get_passport_url(data):
    return AddressParser(data).get_passport_url()


def get_and_save_passport_info(fias_id, url):
    house = House.objects.get(fias_id=fias_id)
    house.passport_info = json.dumps(get_passport_info(url), ensure_ascii=False)
    house.save()


def get_and_save_passport_url_and_info(fias_id, data):
    url = get_passport_url(data)
    passport_info = get_passport_info(url)
    house = House.objects.get(fias_id=fias_id)[0]
    house.passport_url = url
    house.passport_info = json.dumps(passport_info, ensure_ascii=False)
    house.save()
