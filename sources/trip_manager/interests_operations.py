import json

from psycopg2 import sql
from sources.recommendation_manager.recommendation_helpers import sort


class InterestsOperations:
    main_interests_dict = {
        0: "Arts",
        1: "Gluten-free Food",
        2: "Theater",
        3: "Turkish Food",
        4: "Entertainment",
        5: "Opera",
        6: "Museum",
        7: "Italian Food",
        8: "Bakery Deserts",
        9: "Music",
        10: "Nightlife",
        11: "Breakfast Spot",
        12: "Landmark",
        13: "Athletics",
        14: "Middle Eastern Food",
        15: "FrenchFood",
        16: "History",
        17: "Bars",
        18: "Sanctuary",
        19: "Cinema",
        20: "GreekFood",
        21: "IndianFood",
        22: "Vegetarian - Vegan Food",
        23: "Festival",
        24: "Books",
        25: "College",
        26: "American Food",
        27: "Outdoors - Recreation",
        28: "Coffee Shop",
        29: "Mexican Food",
        30: "Cafe",
        31: "Wine",
        32: "Seafood",
        33: "Asian Food"
    }

    def __init__(self, rel_db_man):
        self.db_manager = rel_db_man

    def get_main_interests(self):
        return self.main_interests_dict

    def get_all_interests(self):
        sql_string = sql.SQL("SELECT * FROM interests;")
        resp = list()
        interests = self.db_manager.execute_command(sql_string)
        for interest in interests:
            resp.append({
                "id": interest[0],
                "name": u''.format(interest[1])
            })
        return resp

    def get_user_interests(self, args):
        sql_string = sql.SQL(
            "SELECT * FROM user_interest_rel NATURAL JOIN interests ON user_interest_rel.interestid = interests.id WHERE userid='{}'".format(
                args['user_id']))
        all_int_resp = self.db_manager.execute_command(sql_string)
        resp = dict()
        for elem in all_int_resp:
            resp.update(
                {
                    elem[1]: elem[3]
                }
            )
        return resp

    def add_interests_to_user(self, args):
        # each element in interests array must come in [id]
        # add elements where parent id = id for each element
        interests_array = json.loads(args['interests'])
        user_id = args['user_id']
        resp_arr = list()
        delesql = sql.SQL("DELETE FROM user_interest_rel WHERE userid={}".format(user_id))
        resp = self.db_manager.execute_insert(delesql)
        for elem in interests_array:
            sql_string = sql.SQL(
                "INSERT INTO user_interest_rel(userid, interestid) VALUES ({}, '{}')".format(user_id, elem))
            resp = self.db_manager.execute_insert(sql_string)
            resp_arr.append(resp)
        return args if len(resp_arr) > 0 else None

    def delete_interests_of_user(self, args):
        # each element in interests_array must come in
        # again the same.
        interests_array = args['interests']
        user_id = args['user_id']
        resp_arr = list()
        for elem in interests_array:
            sql_string = sql.SQL(
                "DELETE FROM user_interest_rel WHERE userid={} and interestid='{}'".format(user_id, elem))
            resp = self.db_manager.execute_insert(sql_string)
            resp_arr.append(resp)
        return args if len(resp_arr) > 0 else None

    def give_rating_to_venue(self, args):
        sql_string = sql.SQL(
            "SELECT parentid FROM venue INNER JOIN interests_parent_interest_rel ON venue.category_id=interests_parent_interest_rel.interestid WHERE venue_id='{}'".format(
                args['venue_id']))
        venue_parent_id = self.db_manager.execute_command(sql_string)[0][0]
        sql_string = sql.SQL(
            "SELECT COUNT(*) FROM user_venue_rel WHERE user_id={} and venue_id='{}'".format(args['user_id'],
                                                                                          args['venue_id']))
        if_exists = self.db_manager.execute_command(sql_string)
        print if_exists
        if not if_exists or if_exists[0][0] == 0:
            sql_string = sql.SQL(
                "INSERT INTO user_venue_rel (user_rating, user_id, venue_id) VALUES({},{},'{}') ".format(
                    args['user_rating'],
                    args['user_id'],
                    args['venue_id']))
        else:
            sql_string = sql.SQL("UPDATE user_venue_rel SET user_rating={} WHERE user_id={} and venue_id='{}'".format(args['user_rating'],
                                                                                               args['user_id'],
                                                                                               args['venue_id']))
        resp = self.db_manager.execute_insert(sql_string)
        sql_string = sql.SQL(
            "UPDATE user_checkin_rel SET checkin_count[{}+1]=checkin_count[{}+1] + 1 WHERE user_id={} ".format(
                venue_parent_id, venue_parent_id, args['user_id']))
        resp = self.db_manager.execute_insert(sql_string)
        return self.get_rated_venues_of_user(args) if resp else None

    def give_rating_to_user(self, args):
        sql_string = sql.SQL(
            "UPDATE user_user_rel SET user_rating={} WHERE user_id1={} and user_id2={}".format(args['user_rating'],
                                                                                               args['user_id'],
                                                                                               args['user_id2']))
        resp = self.db_manager.execute_insert(sql_string)
        return args if resp else None

    def get_rated_venues_of_user(self, args):
        sql_string = sql.SQL("SELECT * FROM venue "
                             "INNER JOIN city ON city.city_id=venue.city "
                             "INNER JOIN user_venue_rel ON venue.venue_id=user_venue_rel.venue_id "
                             "INNER JOIN interests_parent_interest_rel ON venue.category_id=interests_parent_interest_rel.interestid "
                             "INNER JOIN interests ON interests_parent_interest_rel.parentid=interests.id "
                             "WHERE user_id={};".format(args['user_id']))
        venues = self.db_manager.execute_command(sql_string)
        resp_venue = list()
        for venue in venues:
            resp = {
                'category_name': venue[18],
                'start_hour': venue[1],
                'end_hour': venue[2],
                'venue_id': venue[3],
                'price': str(venue[4]),
                'venue_rating': str(venue[13]) if venue[13] and venue[13] > 0 else str(venue[5]),
                'image_url': venue[6],
                'venue_name': venue[7].replace('"', "'"),
                'city': venue[10],
                'user_rating': str(venue[14])
            }

            resp_venue.append(resp)
        resp_venue = sort(resp_venue)
        return resp_venue
