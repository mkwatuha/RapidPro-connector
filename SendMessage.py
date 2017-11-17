#Class to handle getting contacts from OpenMRS and send messages to RapidPro
from models import Database
import view_model as vm
from settings import RAPIDPRO_HOST, API_TOKEN
import utils as util
from ConnectorUtils import ConnectorUtils
from temba_client.v2 import TembaClient
from temba_client.exceptions import TembaException
import messageutils
from constants import ENROLLMENT_TYPE_ID, KICKOFF_TYPE_ID

class SendMessage:
    """ Send Message class. Gets contacts and send messages """
    def __init__(self, type_id):
        """ Constructor """
        self.type_id = type_id
        self.client = TembaClient(RAPIDPRO_HOST, API_TOKEN)

    def get_openmrs_contacts(self):
        """ Get records function """
        mrs_database = Database().get_openmrs_db()
        connection = vm.get_db_connector(
            mrs_database.hostname,
            mrs_database.username,
            mrs_database.password,
            mrs_database.database
        )
        last_checked = ConnectorUtils().get_last_checked(self.type_id)
        if self.type_id == ENROLLMENT_TYPE_ID:
            last_checked = ConnectorUtils().get_last_checked(self.type_id)
            contacts = vm.get_clients_enrollment_contacts(connection, last_checked)
        elif self.type_id == KICKOFF_TYPE_ID:
            last_checked = ConnectorUtils().get_last_checked(self.type_id)
            contacts = vm.get_kickoff_client_contacts(connection, last_checked)
        else:
            last_checked = ConnectorUtils().get_last_checked(self.type_id)
            contacts = vm.get_clients_enrollment_contacts(connection, last_checked)

        print contacts

        return contacts

    def get_contacts(self):
        """ Get contacts from OpenMRS"""
        contact_list = []
        contacts = self.get_openmrs_contacts()
        last_checked = ConnectorUtils().get_last_checked(self.type_id)
        for contact in contacts:
            urns = [util.urns_parser(contact.number)]
            try:
                contact_obj = self.client.create_contact(name=contact.name, urns=urns)
                contact_list.append(contact_obj)
                print contact_obj.name
                if last_checked < contact.date_created:
                    last_checked = contact.date_created
            except TembaException as ex:
                print  ex

        ConnectorUtils().update_last_checked(last_checked, self.type_id)
        return contact_list

    def get_message(self, name, program=None):
        """ Get message to be sent from message utils """
        return {
            1: messageutils.enrollment_message(name, program),
            2: messageutils.program_kick_off_message(name),
        }.get(self.type_id, messageutils.enrollment_message(name, program))

    def broadcast_message(self):
        """ Method to be called to initiate sending message procedure """
        contact_list = self.get_contacts()
        if contact_list:
            try:
                for contact in contact_list:
                    text = self.get_message(contact.name, contact.program)
                    contacts = [contact]
                    broadcast = self.client.create_broadcast(text, contacts=contacts)
                    print broadcast.text
            except Exception as ex:
                for field, field_errors in ex.errors.iteritems():
                    for field_error in field_errors:
                        print '{} {}'.format(field, field_error)
        
