from sources.foursquare_api_connector.foursquare_connector import FoursquareConnector
import time
from psycopg2 import sql
from recomendation_threads import myThread
from recommendation_helpers import sort, calculate_cosine_similarity, calculate_user_rating, \
    calculate_user_user_similarity, calculate_venue_rating


class RecomendationOper():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_hometown_reccomendations(self, args):
        sql_string_for_user_info = sql.SQL(" SELECT home_city_id from userdb where userid='{}'".format(args['user_id']))
        get_par_sql = sql.SQL("SELECT interestid FROM user_interest_rel WHERE userid='{}'".format(args['user_id']))
        get_par = self.db_manager.execute_command(get_par_sql)
        interests = list()
        for element in get_par:
            sql_string_for_interest = sql.SQL(
                "SELECT interestid FROM interests_parent_interest_rel WHERE parentid = '{}'".format(element[0]))
            get_sub = self.db_manager.execute_command(sql_string_for_interest)
            for elem in get_sub:
                interests.append(elem[0])

        homecity = str(self.db_manager.execute_command(sql_string_for_user_info)[0][0])

        venue_list = list()
        for inter in interests:

            sql_string = sql.SQL("SELECT * FROM venue INNER JOIN city ON venue.city=city.city_id "
                                 "INNER JOIN interests_parent_interest_rel ON venue.category_id=interests_parent_interest_rel.interestid "
                                 "INNER JOIN interests ON interests_parent_interest_rel.parentid=interests.id "
                                 "WHERE city='{}' and category_id='{}' ORDER BY overall_rating DESC LIMIT 50;".format(
                homecity, inter))

            temp = self.db_manager.execute_command(sql_string)

            for element in temp:
                venue_list.append({
                    'category_name': element[14],
                    'start_hour': element[1],
                    'end_hour': element[2],
                    'venue_id': element[3],
                    'price': str(element[4]),
                    'venue_rating': str(element[5]),
                    'image_url': element[6],
                    'venue_name': element[7].replace('"', "'"),
                    'city': element[10],
                    'category_id':element[11]
                })

        venue_list = sort(venue_list)
        for elem in venue_list:
            elem['venue_rating'] = str(elem['venue_rating'])
            elem['price'] = str(elem['price'])

        return venue_list

    def get_explore_reccomendation(self, args):
        # TODO exception case, cold start on a new user
        user_id = args.pop('user_id')
        recomended_local_city = ""
        template = list()
        if 'category_id'in args.keys():
            template.append(" parentid='{}'".format(args.pop('category_id')))
        if 'city_local' in args.keys():
            template.append( " city={}".format(args['city_local']))
            recomended_local_city = " and home_city_id={}".format(args.pop('city_local'))
        if 'rating' in args.keys():
            template.append(" (overall_rating > {} OR similar_rating > {})".format(args['rating'], args.pop('rating')))
        if 'price' in args.keys():
            template.append(" price < {}".format(args['price']))

        parameter = "WHERE "+template[0] if template else ""
        for i in range(len(template)):
            if i != 0:
                parameter += " and " + template[i]

        sql_string = sql.SQL(
            "SELECT * FROM venue "
            "LEFT JOIN user_venue_rel ON venue.venue_id=user_venue_rel.venue_id AND user_venue_rel.user_id={} "
            "INNER JOIN city ON city.city_id=venue.city "
            "INNER JOIN (interests_parent_interest_rel "
            "INNER JOIN interests ON interests_parent_interest_rel.parentid=interests.id) "
            "ON venue.category_id=interests_parent_interest_rel.interestid "
            "{} ORDER BY similar_rating DESC LIMIT 50;".format(user_id,parameter))
        venues = self.db_manager.execute_command(sql_string)
        resp_venue = list()
        for venue in venues:
            resp = {
                'category_name': venue[18],
                'start_hour': venue[1],
                'end_hour': venue[2],
                'venue_id': venue[3],
                'price': str(venue[4]),
                'venue_rating': str(venue[11]) if venue[11] and venue[11] > 0 else str(venue[5]),
                'overall_rating': str(venue[5]),
                'similar_rating': str(venue[11]),
                'image_url': venue[6],
                'venue_name': venue[7].replace('"', "'"),
                'city': venue[14],
                'user_rating': str(venue[12]) if venue[12] else 0
            }

            resp_venue.append(resp)
        resp_venue = sort(resp_venue)
        sql_string = sql.SQL(
            "SELECT * FROM ((userdb INNER JOIN user_user_rel ON userdb.userid=user_user_rel.user_id2) "
            "INNER JOIN city ON city.city_id=userdb.home_city_id) "
            "LEFT JOIN contacts on userdb.userid=contacts.visitor_id or userdb.userid=contacts.local_id "
            "WHERE user_id1={} {} "
            "ORDER BY similar_rating DESC LIMIT 50;".format(
                user_id, recomended_local_city))
        locals = self.db_manager.execute_command(sql_string)
        resp_local = list()
        for local in locals:
            print local
            resp = {
                'user_id': local[0],
                'firstname': local[2],
                'lastname': local[3],
                'email': local[4],
                'pp_link': local[5],
                'home_city': local[16],
                'short_bio': local[7],
                'birth_date': local[8],
                'occupation': local[9],
                'gender': local[10],
                'venue_rating': str(local[13]),
                'given_rating': str(local[14]),
                'cid': local[17],
                'is_message_sent': local[20],
                'status': local[21]
            }
            resp_local.append(resp)
        resp_local = sort(resp_local)

        return {'venues': resp_venue, 'contacts': resp_local}
