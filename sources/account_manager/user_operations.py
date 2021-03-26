from psycopg2 import sql


class UserOperations:
    def __init__(self, rel_db_man):
        self.db_manager = rel_db_man

    def get_user_info(self, args):
        user_id = args['user_id']
        sql_string_user = sql.SQL("SELECT * FROM userdb WHERE userid = '{}'".format(user_id))

        db_resp = self.db_manager.execute_command(sql_string_user)


        city_resp = None
        if db_resp[0][6]:
            sql_string_city = sql.SQL("SELECT city_name FROM city WHERE city_id = '{}'".format(db_resp[0][6]))
            city_resp = self.db_manager.execute_command(sql_string_city)
        if db_resp:
            resp = {
                'user_id': db_resp[0][0],
                'firstname': db_resp[0][2],
                'lastname': db_resp[0][3],
                'email': db_resp[0][4],
                'pp_link': db_resp[0][5],
                'home_city': city_resp[0][0] if city_resp else None,
                'short_bio': db_resp[0][7],
                'birth_date': db_resp[0][8],
                'occupation': db_resp[0][9],
                'gender':db_resp[0][10]
            }
            sql_string = sql.SQL("SELECT * FROM user_interest_rel INNER JOIN interests ON user_interest_rel.interestid = interests.id WHERE userid='{}'".format(args['user_id']))
            all_int_resp = self.db_manager.execute_command(sql_string)
            int_resp = dict()
            for elem in all_int_resp:
                int_resp.update(
                    {
                        elem[1]: elem[3]
                    }
                )
            resp.update({"interests": int_resp})
        else:
            resp = None
        return resp

    def edit_user_info(self, args):
        sql_string = sql.SQL(
            "UPDATE userdb SET firstname='{}', surname='{}', birthdate='{}', occupation='{}', gender='{}', home_city_id='{}' WHERE userid='{}'".format(
                args['firstname'],
                args['surname'],
                args['birthday'],
                args['occupation'],
                args['gender'],
                args['city_id'],
                args['user_id'])
        )
        resp = self.db_manager.execute_insert(sql_string)
        return args if resp else None

    def delete_user(self, args):
        sql_string = sql.SQL("DELETE FROM userdb WHERE userid={}".format(args['user_id']))
        resp = self.db_manager.execute_insert(sql_string)
        return args if resp else None

    def auth_user(self, args):
        sql_string_user = sql.SQL("SELECT * FROM userdb WHERE userid = '{}'".format(args['user_id']))
        db_resp = self.db_manager.execute_command(sql_string_user)
        if db_resp:
            return args
        return None
