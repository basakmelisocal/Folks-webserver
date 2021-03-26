import hashlib
import validate_email
from psycopg2 import sql


class RegistrationOperations:
    def __init__(self, rel_db_man):
        self.db_manager = rel_db_man

    def login(self, args):
        args['password'] = self.encrypt_pwd(args['password'])
        resp = self.get_user_id(args['email'], args['password'])
        return resp

    def signup(self, args):
        args['password'] = self.encrypt_pwd(args['password'])
        sql_string = sql.SQL(
            "INSERT INTO userdb (firstname, profile_picture_link, short_bio, surname, email, pwd) VALUES ('', '', '', '', '{}', '{}')".format(
                args['email'].lower(), args['password']))
        resp = self.db_manager.execute_insert(sql_string)
        if resp:
            resp = self.get_user_id(args['email'], args['password'])
            checkin_vect = sql.SQL(
                "INSERT INTO user_checkin_rel(user_id, checkin_count) VALUES ({}, ARRAY [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] )".format(
                    resp['user_id']))
            self.db_manager.execute_insert(checkin_vect)
        return resp

    def alter_user(self, args):
        city_id = self._get_city_id(args["home_city"])

        sql_string = sql.SQL(
            "UPDATE userdb SET firstname='{}', surname='{}', birthdate='{}', occupation='{}', gender='{}', home_city_id='{}' WHERE userid='{}'".format(
                args['firstname'],
                args['surname'],
                args['birthday'],
                args['occupation'],
                args['gender'],
                city_id if city_id else -1,
                int(args['user_id']))
        )

        resp = self.db_manager.execute_insert(sql_string)
        if resp:
            resp = {'user_id': args['user_id']}
        return resp

    def upload_img(self, args):

        sql_string = sql.SQL(
            "UPDATE userdb SET image_url='{}' WHERE userid='{}'".format(
                args['image_url'],
                args['user_id'])
        )

        resp = self.db_manager.execute_insert(sql_string)
        if resp:
            resp = args
        return resp

    def get_user_id(self, email, password):
        sql_string = sql.SQL(
            "SELECT userid FROM userdb WHERE email = '{}' AND pwd = '{}'".format(email.lower(), password))
        resp = self.db_manager.execute_command(sql_string)
        if resp:
            resp = {'user_id': str(resp[0][0])}
        else:
            resp = {}
        return resp

    @staticmethod
    def encrypt_pwd(pwd):
        return hashlib.sha1(pwd).hexdigest()

    @staticmethod
    def is_valid_email(email):
        return validate_email.validate_email(email, verify=True)

    def _get_city_id(self, city_name):
        sql_str = sql.SQL(
            "SELECT city_id FROM city WHERE city_name='{}' OR city_name LIKE '^{}%' ".format(city_name, city_name))
        resp = self.db_manager.execute_command(sql_str)
        return resp[0][0]
