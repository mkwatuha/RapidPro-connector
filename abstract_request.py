#!/usr/local/lib/python2.7/
#Abstract request class
import requests
from config import auth_config

AUTH = auth_config()

class AbstractSimpleRequest:
    """ Abstract request class """
    def __init__(self, url):
        self.url = url

    def post(self):
        """ Post request """
        response = requests.post(url=self.url)
        return response

    def get(self):
        """ Get request """
        headers = {'Authorization': 'Token '+ AUTH.get_auth_token()}
        response = requests.get(self.url, headers=headers)
        return response

class AbstractDataRequest:
    """ Abstract request class """
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def post(self):
        """ Post request """
        headers = {'Authorization': 'Token '+ AUTH.get_auth_token(), 'Content-Type': 'application/json'}
        print self.data
        response = requests.post(url=self.url, data=self.data, headers=headers)
        print response.text
        return response

    def get(self):
        """ Get request """
        headers = {'Authorization': 'Token '+ AUTH.get_auth_token()}
        response = requests.get(self.url, data=self.data, headers=headers)
        return response
