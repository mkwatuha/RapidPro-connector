#File with methods to build messages

def enrollment_message(name):
    """ Return enrrollment name """
    return 'Welcome {} to the AIHD program'.format(name)

def program_kick_off_message(name):
    """ Return kickoff message"""
    return 'Dear {}, today marks your wellness journey. The secret of getting ahead is getting started. We will wall with you through the journey.'.format(name)

def goal_congratulatory_message(name):
    """ Return congratulatory message """
    return 'Dear {} congratulations on reaching your goal weight, kindly remember to get in touch with your wellness partner for further guidelines.'.format(name)

def completion_message(name):
    """ Return completion cogratulatory message """
    return 'Dear {}, congratulations on completing your wellness journey, this is the begining of a healthy, happy, holistic you. I f you wish to share your story kindly contacct your wellness partner.'.format(name)

def birthday_message(name):
    """ Return birthday message """
    return 'Life should not only be lived it should be celebrated. Happy birthday {}.'.format(name)

def appointment_booking_message(client_name, partner_name, date, time, venue):
    """ Return appointment booking message alert """
    return 'Dear {}, your appointment has been confirmed with {} on {} at {} at {}'.format(client_name, partner_name, date, time, venue)

def missed_appointment_message(client_name, provider_name, date, time, location):
    """ Missed appointment message alert """
    return 'Dear {}, you missed your appointment with {} on {} at {} at {}'.format(client_name, provider_name, date, time, location)
