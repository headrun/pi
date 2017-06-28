from Fullcontact.generic_functions import *
from Fullcontact.db_operations import *

class Insert(object):

    def main(self, profile_url, media_type, emailid):
        con, cur = get_mysql_connection(DB_HOST, DB_NAME, '')
        if media_type == 'twitter':
            print 'need to insert here'

if __name__ == "__main__":
    Insert().main('', '', '', '')

