from models import Database
import view_model as vm
class ConnectorUtils:
    """ Class containing frequently used methods that use  connector db"""

    def __init__(self):
        self.connector_db = Database().get_connector_db()
        self.connector_conn = vm.get_db_connector(
            self.connector_db.hostname,
            self.connector_db.username,
            self.connector_db.password,
            self.connector_db.database
        )

    def update_last_checked(self, last_checked,id_type):
        """ Update last checked value in the coonector database """
        vm.update_last_checked(self.connector_conn, last_checked, id_type)


    def get_last_checked(self,id_val):
        """ Get timestamp of the last checked record  """
        return vm.get_last_modified(self.connector_conn, id_val)
