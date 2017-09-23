#Functions to manipulate openmrs and conector db

from datetime import datetime
import mysql.connector
from mysql.connector import Error
from settings import CONNECTOR_DB_TABLES as tables
from models import ContactNumber, Database

def get_db_connector(hostname, username, password, database):
    """ Return db connector """
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    return conn

def get_contacts(conn, last_checked):
    """ Get contacts from DB """
    #last_checked =datetime.strftime(last_checked, '%Y-%m-%d %H:%M:%S')
    print last_checked
    query = """ SELECT * FROM Users WHERE modified_at >%s """
    data = (last_checked,)
    cur = conn.cursor()
    cur.execute(query, data)
    contacts = []
    for username, Phone, Location, modified in cur.fetchall():
        contact = ContactNumber(username, Phone, modified)
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
