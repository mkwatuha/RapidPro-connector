# Program utils
import logging
import logging.handlers
from models import ContactNumber, Contact
from temba_client.v2.types import Contact as Contact2

def get_logger(level=None):
    """ logging function """
    logging.basicConfig(filename='/home/connector/log.log', level=logging.DEBUG)

    return logging

def urns_parser(number):
    """ convert number to urns acceptable to rapid pro """
    number = parse_phone_number(number)
    return "tel:" + number

def parse_phone_number(number):
    """ check for valid phone number """
    if number[0] == '+' and len(number) == 13:
        return number
    elif number[0] == '0' and len(number) == 10:
        number  = '+254' + number[1:]
        return number
    elif len(number) == 9:
        number  = '+254' + number
        return number

    return number
        

def contact_builder(name, number):
    """ Build and return an instance of Contact """
    urns = [urns_parser(number)]
    contact = Contact(name, urns)
    return contact

def rapidpro_contact_builder(name=None, number=None, group=None, language=None, fields=None):
    """ create and return contact that conforms to rapidpro contact model """
    urns = [urns_parser(number)]
    contact = Contact2()
    contact.name = name
    contact.urns = urns
    return contact

class ContactParser:
    """ Util class to parse contacts  from json to contact object"""
    def __init__(self, results):
        self.results = results

    def contact_numbers_list(self):
        contacts_list = []
        for contact in self.results:
            username = contact.get('name')
            string = contact.get('urns')[0]
            number = string.split(':', 1)[1]

            list_item = ContactNumber(username, number)
            contacts_list.append(list_item)
            print number
            print username
            #print contacts_list[0]

        print contacts_list