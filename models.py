#MOdels file
import json
from api_urls import *
from abstract_request import AbstractSimpleRequest, AbstractDataRequest
from settings import CONNECTOR_DB_SETTINGS,OPENMRS_DB_SETTINGS

class Database:
    """ database class """
    def __init__(self, hostname=None, name=None, password=None, database=None):
        self.hostname = hostname
        self.name = name
        self.password = password
        self.database = database

    def get_connector_db(self):
        """ return connector database object """
        setting = CONNECTOR_DB_SETTINGS
        self.hostname = setting.get('HOSTNAME')
        self.username = setting.get('USERNAME')
        self.password = setting.get('PASSWORD')
        self.database = setting.get('DB_NAME')

        return self

    def get_openmrs_db(self):
        """ return openmrs database object """
        setting = OPENMRS_DB_SETTINGS
        self.hostname = setting.get('HOSTNAME')
        self.username = setting.get('USERNAME')
        self.password = setting.get('PASSWORD')
        self.database = setting.get('DB_NAME')

        return self

class ContactNumber:
    """ Model class that holds contact number """
    def __init__(self, username, number, timestamp=None):
        self.username = username
        self.number = number
        self.timestamp = timestamp

    def __repr__(self):
        """ readable model representation """
        repr_name = '{} {}'.format(self.username, self.number)
        return repr_name.strip()
class OpenMRSContact:
    """ Model that holds contact from openmrs """
    def __init__(self, name, number, date_created, program_name=None):
        """ Constructor """
        self.name = name
        self.number = number
        self.date_created = date_created
        self.program_name = program_name

    def __repr__(self):
        """ readable model representation """
        repr_name = '{} {}'.format(self.name, self.number)
        return repr_name.strip()

class Contact:
    """ Contact class """
    def __init__(self, name=None, urns=None, fields=None, language='eng', ):
        """ Constructor"""
        self.name = name
        self.urns = urns
        if fields:
            self.fields = fields
        language = language

    def save_contact(self):
        """ Send contact to rapid pro contact list """
        data = json.dumps(self.__dict__)
        request = AbstractDataRequest(CONTACTS_URL, data)
        response = request.post()
        return response

    def get_all_contacts(self):
        """ Get all contacts """
        request = AbstractSimpleRequest(CONTACTS_URL)
        response = request.get()
        return response

class BroadCast:
    """ Abstract broadcast model class """
    def __init__(self, urns, contacts, text, broadcast_id=None):
        """ Constructor """
        self.urns = urns
        self.contacts = contacts
        self.text = text
        if broadcast_id:
            self.broadcast_id = broadcast_id

    def post(self):
        """ Send message broadcast """
        data = json.dumps(self.__dict__)
        request = AbstractDataRequest(BROADCASTS_URL, data)
        response = request.post()
        return response
