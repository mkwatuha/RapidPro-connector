# Main connector file
import json
import schedule
import time
from models import Database, Contact, BroadCast
import view_model as vm
from datetime import datetime, timedelta
from settings import RAPIDPRO_HOST, API_TOKEN
import api_requests as api
import utils as util
from temba_client.v2 import TembaClient
from temba_client.v2.types import Contact as TembaContact
from temba_client.exceptions import TembaException

client = TembaClient(RAPIDPRO_HOST, API_TOKEN)

#TODO: replace get connector db to get openmrs db
def get_openmrs_contacts():
    """ Get records function """
    mrs_database = Database().get_openmrs_db()
    connection = vm.get_db_connector(
        mrs_database.hostname,
        mrs_database.username,
        mrs_database.password,
        mrs_database.database
    )
    last_checked = get_last_checked()
    contacts = vm.get_contacts(connection, last_checked)

    print contacts

    return contacts

def get_last_checked():
    """ Get latest timestamp checked from openmrs """
    database = Database().get_connector_db()
    conn = vm.get_db_connector(
        database.hostname,
        database.username,
        database.password,
        database.database
    )
    last_checked = vm.get_last_modified(conn)

    return last_checked
def update_last_checked(last_checked):
    """ update last checked value in connector db """
    database = Database().get_connector_db()
    conn = vm.get_db_connector(
        database.hostname,
        database.username,
        database.password,
        database.database
    )
    vm.update_last_checked(conn, last_checked)

def schedule_job():
    """ Scheduled job """
    contacts = get_openmrs_contacts()
    last_checked = get_last_checked()
    print last_checked
    for contact in contacts:
        if last_checked < contact.timestamp:
            last_checked = contact.timestamp
    print contacts
    print last_checked
    database = Database().get_connector_db()
    conn = vm.get_db_connector(
        database.hostname,
        database.username,
        database.password,
        database.database
    )
    vm.update_last_checked(conn,last_checked)
    #Send contact to server
    for contact_number in contacts:
        response = None
        contact = util.contact_builder(contact_number.username, contact_number.number)
        try:
            response = contact.save_contact()
        except Exception as error:
            print error
            print error.message
        finally:
            if response:
                print 'sent'
                json_text = json.loads(response.text)
                urns = json_text.get('urns')
                uuid = json_text.get('uuid')
                text = 'Welcome ' + contact.name + " to the Wellness program"
                contact_uuid = [uuid]
                #broadcast = BroadCast(urns, contact_uuid, text)
                #resp = broadcast.post()
                resp = client.create_broadcast(text,urns,None,None)
                print resp
    
def send_message(contact_list):
    """ Send message to contact """
    try:
        for contact in contact_list:
            text = "Welcome " + contact.name + " to the Wellness program"
            contacts = [contact]
            broadcast = client.create_broadcast(text, contacts=contacts)
            print broadcast.text
    except Exception as ex:
        for field, field_errors in ex.errors.iteritems():
            for field_error in field_errors:
                print '{} {}'.format(field, field_error)

def create_contact():
    """ send contact to server"""
    contact_list = []
    contacts = get_openmrs_contacts()
    last_checked = get_last_checked()
    for contact in contacts:
        urns = [util.urns_parser(contact.number)]
        try:
            contact_obj = client.create_contact(name=contact.name, urns=urns)
            contact_list.append(contact_obj)
            print contact_obj.name
            if last_checked < contact.date_created:
                last_checked = contact.date_created
        except TembaException as ex:
            for field, field_errors in ex.errors.iteritems():
                print field_errors

        finally:
            print 'Contact created'

    update_last_checked(last_checked)
    if len(contact_list) > 0:
        send_message(contact_list)


if __name__ == "__main__":
    #schedule.every(2).minutes.do(create_contact)
    '''
    while True:
        schedule.run_pending()
        time.sleep(1) 
    '''

    create_contact()
