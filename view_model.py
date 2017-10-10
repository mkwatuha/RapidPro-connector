#Functions to manipulate openmrs and conector db

from datetime import datetime
import mysql.connector
from mysql.connector import Error
from settings import CONNECTOR_DB_TABLES as tables
from models import ContactNumber, Database, OpenMRSContact

#TODO: Migrate to an ORM

def get_db_connector(hostname, username, password, database):
    """ Return db connector """
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    return conn

def get_contacts(conn, last_checked):
    """ Get contacts from DB """
    #last_checked =datetime.strftime(last_checked, '%Y-%m-%d %H:%M:%S')
    #query = """ SELECT * FROM Users WHERE modified_at >%s """
    query = """ SELECT program.name, patient_program.date_created, person_name.given_name, person_name.middle_name, person_name.family_name, patient_identifier.identifier
      FROM patient_program INNER JOIN program ON patient_program.program_id = program.program_id  
      INNER JOIN patient_identifier ON patient_identifier.patient_id = patient_program.patient_id  
      INNER JOIN person_name ON patient_program.patient_id = person_name.person_id 
      WHERE patient_identifier.identifier_type = %s AND patient_program.date_created>%s; """

    data = (11,last_checked)
    cur = conn.cursor()
    cur.execute(query, data)
    contacts = []
    for program_name, date_created, given_name, middle_name, family_name, identifier in cur.fetchall():
        name = '{} {} {}'.format(given_name, middle_name, family_name)
        contact = OpenMRSContact(name,identifier, program_name)
        contacts.append(contact)

    conn.close()
    return contacts

def get_last_modified(conn):
    """ Get last checked timestamp from connector db """
    cur = conn.cursor()
    last_val = None
    table = str(tables.get('LAST_CHECKED'))
    cur.execute("SELECT * FROM " + table)
    for  last_checked, last_modified, id in cur:
        #last_val = datetime.strptime(last_checked, '%Y-%m-%d %H:%M:%S')
        last_val = last_checked
    conn.close()
    return last_val

def update_last_checked(conn, last_checked):
    """ Update timestamp of last value checked """
    cursor = conn.cursor()
    query = """ UPDATE Last_Checked
                SET last_checked = %s WHERE id=%s"""

    data = (last_checked, 1)
    try:
        # update book title
        cursor = conn.cursor()
        cursor.execute(query, data)
        # accept the changes
        conn.commit()

    except Error as error:
        print error
    finally:
        cursor.close()
        conn.close()
