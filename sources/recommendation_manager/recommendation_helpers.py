from psycopg2 import sql
from sources.foursquare_api_connector.foursquare_connector import FoursquareConnector
import math


def _venue_search(db_manager, category_id_array, city_list, city_name):
    interest_list = list()

    for elem in category_id_array:
        sql_string = sql.SQL("SELECT interestid FROM interests_parent_interest_rel WHERE parentid='{}'".format(elem))
        res = db_manager.execute_command(sql_string)
        if res:
            for i in res:
                interest_list.append(i[0])
    # inputInterest = ','.join(interest_list)
    resp = list()
    for inputInterest in interest_list:
        params = dict(
            v='20130801',
            near=city_list,
            radius="100000",
            intent='browse',
            limit=44,
            categoryId=inputInterest
        )

        fs = FoursquareConnector()
        data = fs.search_venues(params=params)

        venue_list = list()
        try:
            for elem in data['venues']:
                # if city_name in elem['location']['state'].lower() or city_name in elem['location']['city'].lower():
                try:
                    category = elem['categories'][0]['id']
                    temp = {"venue_name": str(elem['name']),
                            "venue_id": str(elem['id']),
                            "category_id": str(category)}
                    venue_list.append(temp)
                except UnicodeEncodeError:
                    pass
        except KeyError:
            pass
        resp.extend(venue_list)
    return resp


def _get_ratings(venue_list):
    venues = list()
    for elem in venue_list:
        venue_data = FoursquareConnector().get_venue_details(elem['venue_id'])
        venue_name = ""
        venue_id = ""
        venue_rating = ""
        category_id = ""
        start_hour = ""
        end_hour = ""
        image_url = ""
        price = ""

        if venue_data.get('venue', None) and venue_data['venue'].get('rating', None):
            if venue_data.get('venue', None) and venue_data['venue'].get('name', None):
                venue_name = str(venue_data['venue']['name'])
                venue_id = str(venue_data['venue']['id'])
                venue_rating = venue_data['venue']['rating']
                category_id = str(venue_data['venue']['categories'][0]['id'])

        if venue_data.get('venue', None) and venue_data['venue'].get('hours', None) and venue_data['venue'][
            'hours'].get('timeframes', None) \
                and venue_data['venue']['hours']['timeframes'][0] and venue_data['venue']['hours']['timeframes'][0].get(
            'open', None) and \
                venue_data['venue']['hours']['timeframes'][0]['open'][0] and \
                venue_data['venue']['hours']['timeframes'][0]['open'][0].get('renderedTime', None):
            renderedTime = str(venue_data['venue']['hours']['timeframes'][0]['open'][0])
            try:
                renderedTime = renderedTime.split("'")
                if renderedTime[3] == '24 Hours':
                    start_hour = '00.00'
                    end_hour = '00.00'
                else:
                    start_hour = renderedTime[3].split(' ')
                    start_hour = start_hour[0]
                    if len(start_hour) != 5:
                        start_hour = '0' + start_hour
                    end_hour = renderedTime[3].split(' ')
                    end_hour = end_hour[1]
                    end_hour = end_hour[8:]
                    if len(end_hour) != 5:
                        end_hour = '0' + end_hour
            except:
                pass

        if venue_data.get('venue', None) and venue_data['venue'].get('price', None) and venue_data['venue'][
            'price'].get('tier', None):
            price = venue_data['venue']['price']['tier']

        if venue_data.get('venue', None) and venue_data['venue'].get('bestPhoto', None) and venue_data['venue'][
            'bestPhoto'].get('suffix', None) \
                and venue_data['venue']['bestPhoto'].get('prefix', None) and venue_data['venue']['bestPhoto'].get(
            'width', None) and venue_data['venue']['bestPhoto'].get('height', None):
            suffix = venue_data['venue']['bestPhoto']['suffix']
            prefix = venue_data['venue']['bestPhoto']['prefix']
            width = venue_data['venue']['bestPhoto']['width']
            height = venue_data['venue']['bestPhoto']['height']
            image_url = str(prefix) + str(width) + "x" + str(height) + str(suffix)

        if venue_name and venue_id and category_id and venue_rating:
            temp = {"venue_name": venue_name,
                    "venue_id": venue_id,
                    "category_id": category_id,
                    "venue_rating": venue_rating,
                    "image_url": image_url,
                    "price": price,
                    "end_hour": end_hour,
                    "start_hour": start_hour
                    }
            venues.append(temp)
    return venues


def merge(left, right):
    result = []
    n, m = 0, 0
    while n < len(left) and m < len(right):
        if left[n]['venue_rating'] >= right[m]['venue_rating']:
            result.append(left[n])
            n += 1
        else:
            result.append(right[m])
            m += 1
    result += left[n:]
    result += right[m:]
    return result


def sort(seq):
    if len(seq) <= 1:
        return seq

    middle = len(seq) / 2
    left = sort(seq[:middle])
    right = sort(seq[middle:])
    return merge(left, right)


def calculate_user_user_similarity(db_manager):
    sql_string = sql.SQL("SELECT userid FROM userdb ORDER BY userid ASC")
    user_list = db_manager.execute_command(sql_string)
    user_count = len(user_list)
    for user in user_list:
        checking_sql = sql.SQL("SELECT checkin_count FROM user_checkin_rel WHERE user_id='{}'".format(user[0]))
        resp = db_manager.execute_command(checking_sql)
        if not resp:
            checkin_vect = sql.SQL(
                "INSERT INTO user_checkin_rel(user_id, checkin_count) VALUES ({}, ARRAY [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] )".format(
                    user[0]))
            db_manager.execute_insert(checkin_vect)

    for i in range(0, user_count):
        for j in range(i + 1, user_count):
            user_id1 = user_list[i][0]
            user_id2 = user_list[j][0]
            sql_string = sql.SQL(
                'SELECT checkin_count FROM user_checkin_rel WHERE user_id={} OR user_id={}'.format(user_id1,
                                                                                                           user_id2))
            res = db_manager.execute_command(sql_string)
            array1 = res[0][0]
            array2 = res[1][0]

            similarity = calculate_cosine_similarity(array1, array2)

            sql_string = sql.SQL(
                "UPDATE user_user_similarity SET similarity = {} WHERE (user_id1 = {} AND user_id2 = {}) OR (user_id1 = {} AND user_id2 = {})".format(
                    float(similarity), int(user_id1), int(user_id2), int(user_id2), int(user_id1)))
            db_manager.execute_insert(sql_string)


def calculate_cosine_similarity(v1, v2):
    sum = 0
    square_v1 = 0
    square_v2 = 0
    for i in range(0, len(v1)):
        if v1[i] == None:
            v1[i] = 0
        if v2[i] == None:
            v2[i] = 0
        sum = sum + (v1[i] * v2[i])
        square_v1 = square_v1 + (v1[i] * v1[i])
        square_v2 = square_v2 + (v2[i] * v2[i])
    root_v1 = math.sqrt(square_v1)
    root_v2 = math.sqrt(square_v2)

    if float(root_v1 * root_v2) != 0:
        similarity = float(sum) / float(root_v1 * root_v2)
    else:
        similarity = 0
    return similarity


def calculate_venue_rating(db_manager):
    sql_string = sql.SQL("SELECT userid FROM userdb ORDER BY userid ASC")
    user_list = db_manager.execute_command(sql_string)
    user_count = len(user_list)

    for i in range(0, user_count):

        user_id = user_list[i][0]
        sql_string = sql.SQL("SELECT checkin_count FROM user_checkin_rel WHERE user_id='{}'".format(user_id))
        res = db_manager.execute_command(sql_string)
        array1 = res[0][0]
        total_checkin_count = sum(array1)

        if total_checkin_count >= 5:
            sql_string = sql.SQL("SELECT venue_id FROM venue")
            venue_list_user = db_manager.execute_command(sql_string)
            venue_count = len(venue_list_user)

            for j in range(0, venue_count):

                venue_id = venue_list_user[j][0]
                sum_below = 0
                sum_above = 0

                sql_string = sql.SQL("SELECT user_id FROM user_venue_rel WHERE venue_id = '{}'".format(venue_id))
                user_list2 = db_manager.execute_command(sql_string)
                user_count2 = len(user_list2)

                if user_count2 > 0:

                    for m in range(0, user_count2):

                        other_id = user_list2[m][0]
                        if user_id != other_id:
                            sql_string = sql.SQL(
                                "SELECT checkin_count FROM user_checkin_rel WHERE user_id='{}'".format(
                                    other_id))
                            res = db_manager.execute_command(sql_string)
                            array2 = res[0][0]
                            total_checkin_count_other = sum(array2)

                            if total_checkin_count_other >= 5:
                                sql_string = sql.SQL(
                                    "SELECT * FROM user_venue_rel WHERE user_id = '{}' AND venue_id = '{}'".format(
                                        other_id, venue_id))
                                other_venue_list = db_manager.execute_command(sql_string)
                                other_rating = other_venue_list[0][3]

                                sql_string = sql.SQL(
                                    "SELECT * FROM user_user_similarity WHERE (user_id1 = '{}' AND user_id2 = '{}') OR (user_id1 = '{}' AND user_id2 = '{}')".format(
                                        user_id, other_id, other_id, user_id))
                                other_user_similarity = db_manager.execute_command(sql_string)
                                similarity = other_user_similarity[0][2]
                                print similarity
                                sum_above = sum_above + float(similarity * other_rating)
                                sum_below = sum_below + similarity

                    print sum_below, sum_above
                    if sum_below != 0:
                        new_rating = float(sum_above) / float(sum_below)
                    else:
                        new_rating = 0
                    print new_rating, venue_id

                    sql_string = sql.SQL(
                        "SELECT user_rating FROM user_venue_rel WHERE user_id = '{}' AND venue_id = '{}'".format(
                            user_id, venue_id))
                    res = db_manager.execute_command(sql_string)

                    if res:
                        sql_string = sql.SQL(
                            "UPDATE user_venue_rel SET similar_rating = '{}' WHERE user_id = '{}' AND venue_id = '{}'".format(
                                new_rating, user_id, venue_id))
                    else:
                        sql_string = sql.SQL(
                            "INSERT INTO user_venue_rel (user_id, venue_id, similar_rating) VALUES ('{}', '{}', '{}')".format(
                                user_id, venue_id, new_rating))
                    db_manager.execute_insert(sql_string)



def calculate_user_rating(db_manager):
    sql_string = sql.SQL("SELECT userid FROM userdb")
    user_list = db_manager.execute_command(sql_string)
    user_count = len(user_list)

    for i in range(0, user_count):

        user_id = user_list[i][0]

        for j in range(0, user_count):

            user_id2 = user_list[j][0]

            if user_id != user_id2:
                sum_below = 0
                sum_above = 0

                sql_string = sql.SQL("SELECT user_id1 FROM user_user_rel WHERE user_id2 = '{}'".format(user_id2))
                user3_list = db_manager.execute_command(sql_string)
                user3_count = len(user3_list)

                if user3_count > 0:

                    for m in range(0, user3_count):

                        other_id = user3_list[m][0]
                        if user_id != other_id:
                            sql_string = sql.SQL(
                                "SELECT * FROM user_user_rel WHERE user_id1 = '{}' AND user_id2 = '{}'".format(other_id,
                                                                                                               user_id2))
                            other_venue_list = db_manager.execute_command(sql_string)
                            other_rating = other_venue_list[0][3]

                            sql_string = sql.SQL(
                                "SELECT * FROM user_user_similarity WHERE user_id1 = '{}' AND user_id2 = '{}'".format(
                                    user_id, other_id))
                            other_user_similarity = db_manager.execute_command(sql_string)
                            similarity = other_user_similarity[0][2]

                            sum_above = sum_above + float(similarity * other_rating)
                            sum_below = sum_below + similarity

                    if sum_below != 0:
                        new_rating = float(sum_above) / float(sum_below)
                    else:
                        new_rating = 0

                    sql_string = sql.SQL(
                        "SELECT user_rating FROM user_user_rel WHERE user_id1 = '{}' AND user_id2 = '{}'".format(
                            user_id, user_id2))
                    res = db_manager.execute_command(sql_string)

                    if res:
                        sql_string = sql.SQL(
                            "UPDATE user_user_rel SET similar_rating = '{}' WHERE user_id1 = '{}' AND user_id2 = '{}'".format(
                                new_rating, user_id, user_id2))
                    else:
                        sql_string = sql.SQL(
                            "INSERT INTO user_user_rel (user_id1, user_id2, similar_rating) VALUES ('{}', '{}', '{}')".format(
                                user_id, user_id2, new_rating))
                    db_manager.execute_insert(sql_string)
