# Settings file. Set app settings here


# TODO: Put token in environment
API_TOKEN = 'f8452af03fee45dba004754aecc463a34d291042'

RAPIDPRO_HOST = 'http://127.0.0.1:8000'
OPENMRS_DB_SETTINGS = {
    'DB_NAME':'openmrs',
    'USERNAME':'openmrs',
    'PASSWORD':'password',
}

CONNECTOR_DB_SETTINGS = {
    'DB_NAME':'TRIAL',
    'HOSTNAME':'localhost',
    'USERNAME':'root',
    'PASSWORD':'password',
}

CONNECTOR_DB_TABLES = {
    "LAST_CHECKED":'Last_Checked',
    "USERS":'Users',
}

OPENMRS_DB_TABLES = {
    'PROGRAMS':'program',
    'PATIENT_PROGRAM':'patient_program',
    'PHONE_NUMBERS':'patient_identifier',
    'IDENTIFIER_TYPE':'patient_identifier_type',
}
