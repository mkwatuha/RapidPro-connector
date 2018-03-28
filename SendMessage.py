#Class to handle getting contacts from OpenMRS and send messages to RapidPro
from models import Database
import view_model as vm
from settings import RAPIDPRO_HOST, API_TOKEN
import utils as util
from ConnectorUtils import ConnectorUtils
from temba_client.v2 import TembaClient
from temba_client.exceptions import TembaException
import messageutils
from constants import ENROLLMENT_TYPE_ID, KICKOFF_TYPE_ID, BIRTHDAY_TYPE_ID,APPOINTMENT_REMINDER_TYPE_ID, VENUE

class SendMessage:
    """ Send Message class. Gets contacts and send messages """
    def __init__(self, type_id):
        """ Constructor """
        self.type_id = type_id
        self.client = TembaClient(RAPIDPRO_HOST, API_TOKEN)

    def get_openmrs_contacts(self):
        """ Get contacts from OPENMRS """
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
        elif self.type_id == BIRTHDAY_TYPE_ID:
            contacts = vm.get_birthday_contacts(connection)
        elif self.type_id == APPOINTMENT_REMINDER_TYPE_ID:
            contacts = vm.get_appointment_booking_contacts(connection, last_checked)
        elif self.type_id == MISSED_APPOINTMENT_NOTIFICATION_TYPE_ID:
            contacts = vm.get_missed_appointment_client_contacts(connection, last_checked)
        else:
            last_checked = ConnectorUtils().get_last_checked(self.type_id)
            contacts = vm.get_clients_enrollment_contacts(connection, last_checked)

        return contacts

    def check_contacts(self, contacts):
        """ Check if openmrs contact is saved in rapidpro. Returns a collection of rapidpro contacts"""
        contact_list = []
        last_checked = ConnectorUtils().get_last_checked(self.type_id)
        for contact in contacts:
            urn = util.urns_parser(contact.number)
            try:
                temba_contact = self.client.get_contacts(urn=urn).first()
                if temba_contact:
                    #If contact is found
                    contact_list.append(temba_contact)
                    if last_checked < contact.date_created:
                        last_checked = contact.date_created
                else:
                    #contact not found, save to rapidpro first
                    try:
                        contact_obj = self.client.create_contact(name=contact.name, urns=[urn])
                        contact_list.append(contact_obj)

                        if last_checked < contact.date_created:
                            last_checked = contact.date_created
                    except TembaException as ex:
                        contact_list.append(None)
                        print  ex
            except TembaException as ex:
                contact_list.append(None)
                print ex;
        ConnectorUtils().update_last_checked(last_checked, self.type_id)
        return contact_list

    def get_contacts(self):
        """ Get contacts from OpenMRS and send to RapidPro"""
        contact_list = []
        contacts = self.get_openmrs_contacts()
        last_checked = ConnectorUtils().get_last_checked(self.type_id)
        for contact in contacts:
            urns = [util.urns_parser(contact.number)]
            try:
                contact_obj = self.client.create_contact(name=contact.name, urns=urns)
                contact_list.append(contact_obj)

                if last_checked < contact.date_created:
                    last_checked = contact.date_created
            except TembaException as ex:
                print  ex

        ConnectorUtils().update_last_checked(last_checked, self.type_id)
        return contact_list

    def get_message(self, name, provider=None, start_date=None):
        """ Get message to be sent from message utils """
        return {
            1: messageutils.enrollment_message(name),
            2: messageutils.program_kick_off_message(name),
            3: messageutils.birthday_message(name),
            4: messageutils.appointment_booking_message(name, provider, start_date, start_date, VENUE),
            5:messageutils.missed_appointment_message(name, provider, start_date, start_date, VENUE)
        }.get(self.type_id, messageutils.enrollment_message(name))

    def broadcast_message(self):
        """ Method to be called to initiate sending message procedure """
        openmrs_contacts = self.get_openmrs_contacts()
        contact_list = self.check_contacts(openmrs_contacts)

        if self.type_id == APPOINTMENT_REMINDER_TYPE_ID:
            if contact_list:
                for index,contact in enumerate(contact_list):
                    
                    if openmrs_contacts[index]:
                        contact_obj = openmrs_contacts[index]
                        text = self.get_message(contact_obj.name, contact_obj.provider_name, contact_obj.start_date, contact_obj.start_date)
                        contacts = [contact]
                        try:
                            broadcast = self.client.create_broadcast(text, contacts=contacts)
                        except Exception as ex:
                            for field, field_errors in ex.errors.iteritems():
                                for field_error in field_errors:
                                    print '{} {}'.format(field, field_error)
        else:
            for contact in contact_list:
                text = self.get_message(contact.name)
                contacts=[contact]
                try:
                    broadcast = self.client.create_broadcast(text, contacts=contacts)
                except Exception as ex:
                    for field, field_errors in ex.errors.iteritems():
                        for field_error in field_errors:
                            print '{} {}'.format(field, field_error)
        
