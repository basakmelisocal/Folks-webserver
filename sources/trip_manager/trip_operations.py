from psycopg2 import sql


class TripOperations:
    def __init__(self, rel_db_man):
        self.db_manager = rel_db_man

    def get_trips_of_user(self, args):
        city=""
        if args.get('city_id', None):
            city= 'and city={}'.format(args['city_id'])
        sql_string = sql.SQL("SELECT trip_id FROM trip WHERE user_id = {} {}".format(args['user_id'], city))
        trips = self.db_manager.execute_command(sql_string)
        resp = list()
        for t in trips:
            resp.append(self.get_trip_and_contents(args={'trip_id':t[0], 'user_id':args['user_id'] }))
        return resp


    def add_trip_to_user(self, args):
        sql_string_to_insert_trip = sql.SQL(
            "INSERT INTO trip(user_id, city_id, start_date, end_date ) VALUES ({}, {}, '{}','{}')"
                .format(args['user_id'], args['city_id'], args['start_date'], args['end_date']))
        resp = self.db_manager.execute_insert(sql_string_to_insert_trip)
        if resp:
            return args
        else:
            return None

    def edit_trip_of_user(self, args):
        sql_string = sql.SQL("UPDATE trip SET city_id = '{}', start_date = '{}', end_date = '{}' "
                             "WHERE trip_id = {}"
                             "AND user_id = {}".format(args['city_id'], args['start_date'], args['end_date'],
                                                       args['trip_id'], args['user_id']))
        resp = self.db_manager.execute_insert(sql_string)
        if resp:
            return args
        else:
            return None

    def delete_trip_of_user(self, args):
        sql_string = sql.SQL(
            "DELETE FROM trip_venue_rel WHERE trip_id ={}".format(int(args['trip_id'])))
        resp = self.db_manager.execute_insert(sql_string)
        sql_string = sql.SQL(
            "DELETE FROM trip WHERE user_id = {} AND trip_id = {}".format(args['user_id'], int(args['trip_id'])))
        resp = self.db_manager.execute_insert(sql_string)
        if resp:
            return args
        else:
            return None

    def add_venue_to_trip(self, args):
        venue_info = sql.SQL("SELECT * FROM venue WHERE venue_id='{}'".format(args['venue_id']))
        trip_info = sql.SQL("SELECT * FROM trip WHERE trip_id='{}'".format(args['trip_id']))

        if venue_info[0][8] == trip_info[0][1]:
            sql_string = sql.SQL(
                "INSERT INTO trip_venue_rel(trip_id, venue_id) VALUES('{}','{}')".format(args['trip_id'], args['venue_id'])
            )
            self.db_manager.execute_insert(sql_string)
            return self.get_trip_and_contents(args)
        return {'error': 'Trip and venue city mismatch'}

    def delete_venue_of_trip(self, args):
        sql_string = sql.SQL(
            "DELETE FROM trip_venue_rel WHERE trip_id={} and venue_id={}".format(args['trip_id'], args['venue_id'])
        )
        self.db_manager.execute_insert(sql_string)
        return self.get_trip_and_contents(args)

    def get_cities(self):
        sql_str = sql.SQL("SELECT * FROM city")
        resp = self.db_manager.execute_command(sql_str)
        return resp

    def get_trip_and_contents(self, args):
        sql_string_venues = sql.SQL(
            "SELECT * FROM trip_venue_rel INNER JOIN venue ON trip_venue_rel.venue_id=venue.venue_id "
            "INNER JOIN interests_parent_interest_rel ON venue.category_id=interests_parent_interest_rel.interestid "
            "INNER JOIN interests ON interests_parent_interest_rel.parentid=interests.id "
            "LEFT JOIN user_venue_rel ON venue.venue_id=user_venue_rel.venue_id and user_venue_rel.user_id={} "
            "WHERE trip_id = {}".format(args['user_id'],args['trip_id']))
        sql_string_trip = sql.SQL(
            "SELECT * FROM trip INNER JOIN city ON city.city_id=trip.city_id WHERE trip_id={}".format(args['trip_id']))

        venues = self.db_manager.execute_command(sql_string_venues)
        trip = self.db_manager.execute_command(sql_string_trip)
        resp = None
        if trip:
            resp = {
                'trip_id': trip[0][0],
                'city_id': trip[0][1],
                'start_date': trip[0][2],
                'end_date': trip[0][3],
                'user_id': trip[0][4],
                'city': trip[0][6],
                'venues': list()
            }
            for v in venues:
                resp['venues'].append({
                    'venue_id': v[1],
                    'interest_id': v[2],
                    'start_hour': v[3],
                    'end_hour': v[4],
                    'price': str(v[6]),
                    'overall_rating': str(v[17]) if v[17] else str(v[7]),
                    'image_url': v[8],
                    'venue_name': v[9],
                    'city': v[10],
                    'interest_name': v[14],
                    'my_rating':str(v[18]) if v[18] else 0

                })

        return resp if resp else {}
