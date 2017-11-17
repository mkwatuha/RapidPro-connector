# Settings file. Set app settings here


# TODO: Put token in environment
API_TOKEN = '952c3dbad9bbef5f75aa5d137bf0ba291ace5f4c'

RAPIDPRO_HOST = 'http://45.79.138.76'
OPENMRS_DB_SETTINGS = {
    'DB_NAME':'openmrs',
    'HOSTNAME':'localhost',
    'USERNAME':'root',
    'PASSWORD':'password',
}

CONNECTOR_DB_SETTINGS = {
    'DB_NAME':'TRIAL',
    'HOSTNAME':'localhost',
    'USERNAME':'root',
    'PASSWORD':'password',
}

CONNECTOR_DB_TABLES = {
    "LAST_CHECKED":"Last_Checked",
    "USERS":'Users',
}

OPENMRS_DB_TABLES = {
    'PROGRAMS':'program',
    'PATIENT_PROGRAM':'patient_program',
    'PHONE_NUMBERS':'patient_identifier',
    'IDENTIFIER_TYPE':'patient_identifier_type',
}
