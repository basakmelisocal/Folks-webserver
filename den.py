import random

from sources.data_manager.rel_db_manager import RelationalDBManager as DBManager
from psycopg2 import sql


def init_user_user_similarity():
    db_manager = DBManager()
    sql_string = sql.SQL("SELECT userid FROM userdb")
    user_list = db_manager.execute_command(sql_string)
    user_count = len(user_list)

    for i in range(0, user_count):
        for j in range(i + 1, user_count):
            user_id1 = user_list[i][0]
            user_id2 = user_list[j][0]
            sql_string = sql.SQL(
                "INSERT INTO user_user_similarity (user_id1, user_id2, similarity) VALUES ('{}', '{}', '{}')"
                    .format(user_id1, user_id2, 0))
            db_manager.execute_insert(sql_string)


def ratings_given_by_users():
    db_manager = DBManager()
    sql_string = sql.SQL("SELECT userid FROM userdb")
    user_list = db_manager.execute_command(sql_string)
    user_count = len(user_list)
    for elem in user_list:
        interests_sql = sql.SQL("SELECT interestid FROM user_interest_rel WHERE userid = {}".format(elem[0]))
        interests = db_manager.execute_command(interests_sql)
        for interest in interests:
            venues_sql = sql.SQL("SELECT venue_id "
                                 "FROM venue inner join interests_parent_interest_rel on interests_parent_interest_rel.interestid=venue.category_id "
                                 "where interests_parent_interest_rel.parentid='{}' LIMIT 3;".format(interest[0]))
            venues = db_manager.execute_command(venues_sql)
            for venue in venues:
                rating = random.random() * 10
                while int(rating) == 0:
                    rating = random.random() * 2 + 8
                # rating_sql = sql.SQL("insert into user_venue_rel(user_id, venue_id, user_rating) values ( '{}','{}', '{}')".format(elem[0], venue[0], rating))
                rating_sql = sql.SQL(
                    "update user_venue_rel set  user_rating='{}' where user_id='{}' and venue_id='{}';".format(rating,
                                                                                                               elem[0],
                                                                                                               venue[
                                                                                                                   0]))
                db_manager.execute_insert(rating_sql)


def init_user_user_rel():
    db_manager = DBManager()
    sql_string = sql.SQL("SELECT userid FROM userdb")
    user_list = db_manager.execute_command(sql_string)
    user_count = len(user_list)

    for i in range(0, user_count):
        for j in range(i + 1, user_count):
            user_id1 = user_list[i][0]
            user_id2 = user_list[j][0]
            sql_string = sql.SQL(
                "INSERT INTO user_user_rel (user_id1, user_id2, similar_rating, user_rating) VALUES ('{}', '{}', {}, {})"
                    .format(user_id1, user_id2, 0, 0))
            db_manager.execute_insert(sql_string)

if __name__ == '__main__':
    init_user_user_rel()
