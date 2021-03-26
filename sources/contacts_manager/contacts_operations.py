from psycopg2 import sql
from sources.account_manager.accountmanager import AccountManager
class ContactsOper():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_contact_recommendation(self, args):
        # MEL
        pass

    def send_contact_request(self, args):
        sql_string = sql.SQL("INSERT INTO contacts (visitor_id, local_id) VALUES({}, {});".format(args['user_id'], args['local_id']))
        self.db_manager.execute_insert(sql_string)
        return args

    def accept_or_reject_request(self, args):
        sql_string = sql.SQL("UPDATE contacts SET request_status={} WHERE visitor_id={} and local_id={}".format(args['request_status'], int(args['visitor_id']), int(args['user_id'])))
        resp = self.db_manager.execute_insert(sql_string)
        return args

    def get_pending_requests(self, args):
        sql_string = sql.SQL("SELECT * FROM contacts WHERE (local_id={}) and request_status=0;".format(args['user_id'],args['user_id']))
        resp = self.db_manager.execute_command(sql_string)
        matches = list()
        for contact_data in resp:
            match_user = dict()
            if contact_data[1] == int(args['user_id']):
                match_user = AccountManager.user_operations.get_user_info({'user_id':contact_data[2]})
            elif contact_data[2] == int(args['user_id']):
                match_user = AccountManager.user_operations.get_user_info({'user_id':contact_data[1]})
            if match_user:
                match_user['cid'] = contact_data[0]
                match_user['request_status'] = contact_data[4]
                matches.append(match_user)
        return matches

    def get_contacts(self, args):
        sql_string = sql.SQL("SELECT * FROM contacts WHERE (visitor_id={} or local_id={}) and request_status=1;".format(args['user_id'], args['user_id']))
        resp = self.db_manager.execute_command(sql_string)
        matches = list()
        for contact_data in resp:
            match_user = dict()
            if contact_data[1] == int(args['user_id']):
                match_user = AccountManager.user_operations.get_user_info({'user_id': contact_data[2]})
            elif contact_data[2] == int(args['user_id']):
                match_user = AccountManager.user_operations.get_user_info({'user_id': contact_data[1]})
            if match_user:
                match_user['cid'] = contact_data[0]
                match_user['request_status'] = contact_data[4]
                matches.append(match_user)
        return matches


