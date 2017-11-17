# Main connector file
import time
import schedule
from constants import KICKOFF_TYPE_ID, ENROLLMENT_TYPE_ID
from SendMessage import SendMessage


if __name__ == "__main__":
    schedule.every(2).minutes.do(SendMessage(ENROLLMENT_TYPE_ID).broadcast_message())
    schedule.every(5).minutes.do(SendMessage(KICKOFF_TYPE_ID).broadcast_message())
    while True:
        schedule.run_pending()
        time.sleep(1)

    #create_contact()
    #print ConnectorUtils().get_last_checked(ENROLLMENT_TYPE_ID)
    #SendMessage(ENROLLMENT_TYPE_ID).broadcast_message()
    #SendMessage(KICKOFF_TYPE_ID).broadcast_message()
