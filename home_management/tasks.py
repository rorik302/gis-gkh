from home_management.parsers import PassportParser, AddressParser


def get_passport_info(url):
    return PassportParser(url).get_passport_info()


def get_passport_url(data):
    return AddressParser(data).get_passport_url()
