# Main connector file
import json
import schedule
import time
from constants import KICKOFF_TYPE_ID, ENROLLMENT_TYPE_ID
from SendMessage import SendMessage


if __name__ == "__main__":
    #schedule.every(2).minutes.do(create_contact)
    '''
    while True:
        schedule.run_pending()
        time.sleep(1) 
    '''

    #create_contact()
    #print ConnectorUtils().get_last_checked(ENROLLMENT_TYPE_ID)
    #SendMessage(ENROLLMENT_TYPE_ID).broadcast_message()
    SendMessage(KICKOFF_TYPE_ID).broadcast_message()
