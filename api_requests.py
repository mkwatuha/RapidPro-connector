#API calls to the rapidpro server

import json
from abstract_request import AbstractSimpleRequest
from api_urls import CONTACTS_URL, BROADCASTS_URL, GROUPS_URL
def get_all_contacts():
    """ Get all contacts from rapid pro"""
    request = AbstractSimpleRequest(CONTACTS_URL)
    response = request.get()
    json_text = json.loads(response.text)
    print json_text.get('results')
    print len(json_text)
    return json_text

def get_all_broadcasts():
    """ Obtain broadcast json list from rapid Pro """
    request = AbstractSimpleRequest(BROADCASTS_URL)
    response = request.get()
    json_text = json.loads(response.text)
    print json_text
    return json_text

def get_all_groups():
    """ Obtain all groups"""
    request = AbstractSimpleRequest(GROUPS_URL)
    response = request.get()
    json_text = json.loads(response.text)
    return json_text

