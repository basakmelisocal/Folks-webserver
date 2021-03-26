import datetime
from sources.account_manager.accountmanager import AccountManager
from psycopg2 import sql


class MessageOper():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def push_message_to_db(self, args):
        sql_string = sql.SQL("SELECT COUNT(*) FROM message WHERE contact_id=" + args['contact_id'] + " LIMIT 1")
        count = self.db_manager.execute_command(sql_string)
        if count[0][0] == 0:
            sql_string = sql.SQL("UPDATE contacts SET is_message_sent=true WHERE cid=" + args['contact_id'])
            self.db_manager.execute_insert(sql_string)

        sql_string = sql.SQL(
            "INSERT INTO message(senderid, recieverid, contact_id, message, date) VALUES ({}, {}, {}, '{}', '{}')".format(
                args['user_id'], args['reciever_id'], args['contact_id'], args['message'], args['date']))
        resp = self.db_manager.execute_insert(sql_string)

        if resp:
            return args
        else:
            return None

    def send_read_info(self, args):
        sql_string = sql.SQL(
            "UPDATE messages SET is_read=true WHERE recieverid={} AND contact_id={}".format(args['user_id'],
                                                                                            args['contact_id']))
        resp = self.db_manager.execute_insert(sql_string)
        if resp:
            return args
        else:
            return None

    def pull_conversation(self, args):
        sql_string = sql.SQL("SELECT * FROM message WHERE contact_id={}".format(args['contact_id']))
        resp_message = self.db_manager.execute_command(sql_string)
        resp = list()
        for message in resp_message:
            message_dict = {
                'sender_id': message[0],
                'reciever_id': message[1],
                'message': message[2],
                'contact_id': message[3],
                'is_read': message[4],
                'date': message[5]

            }
            resp.append(message_dict)
        return resp

    def pull_new_messages(self, args):
        sql_string = sql.SQL("SELECT * FROM message WHERE recieverid={} and is_read=false".format(args['user_id']))
        resp_message = self.db_manager.execute_command(sql_string)
        resp = list()
        for message in resp_message:
            message_dict = {
                'sender_id': message[0],
                'reciever_id': message[1],
                'message': message[2],
                'contact_id': message[3],
                'is_read': message[4],
                'date': message[5]

            }
            resp.append(message_dict)
        return resp

    def get_conversation_list(self, args):
        sql_string = sql.SQL(
            "SELECT * FROM contacts WHERE (local_id={} OR visitor_id={}) AND is_message_sent=true".format(
                args['user_id'], args['user_id']))
        resp_message = self.db_manager.execute_command(sql_string)
        matches = list()
        for contact_data in resp_message:
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

    def delete_conversation(self, args):
        pass