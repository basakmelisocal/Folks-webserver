# coding=utf-8
import ast
import json
import pickle

from sources.foursquare_api_connector import foursquare_connector
from sources.data_manager import rel_db_manager
from sources.recommendation_manager.recomendation_threads import myThread
from sources.recommendation_manager.recommendation_helpers import sort
from psycopg2 import sql


def venue_add():
    a = rel_db_manager.RelationalDBManager()
    interests = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                 '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33']
    city_dict = {
        '1': [
            'Cankaya',
            'Yenimahalle',
            'Mamak',
            'Kecioren',
            'Sincan',
            'Altindag',
            'Etimesgut',
            'Golbasi',
            'Kavaklidere',
            'Bahcelievler',
            'Anittepe',
            'Kucukesat',
            'Ayranci',
            'Yasamkent',
            'Ulus',
            'Kizilay',
            'Oran',
            'Yildiz',
            'Cayyolu',
            'Bilkent',
            'Cukurambar',
        ],
        '2': [
            'Besiktas',
            'Beyoglu',
            'Arnavutkoy',
            'Beykoz',
            'Sisli',
            'Kadikoy',
            'Adalar',
            'Atasehir',
            'Fatih',
            'Bahcelievler',
            'Sariyer',
            'Kalamis', 'Kuzguncuk', 'Beykoz', 'Arnavutkoy', 'Moda', 'Bagdat Caddesi', 'Rumeli Hisari', 'Eminonu',
            'Cihangir',
            'Kilyos',
            'Garipce', 'Kavaklar', 'Sisli', 'Taksim', 'Besiktas', 'Adalar', 'Balat', 'Sultanahmet', 'Galata'

        ],
        '3': [
            'Karsiyaka',
            'Guzelbahce',
            'Bornova',
            'Foca',
            'Cesme',
            'Konak',
            'Buca',
            'Dikili',

            'Konak',
            'Kemeralti',
            'Cesme',
            'Cesmealti',
            'Selcuk',
            'Alsancak',
            'Goztepe',
            'Bostanli',
            'Kordon',
            'Asansor',
            'Urla',
            'Alacati',
            'Eski Foca',
            'Seferihisar',
            'Ozdere',
            'Balikliova',
            'Demircili',
            'Balcova',
            'Sasali',
            'Smyra',
            'Inciralti',
            'Sirince'
        ]
    }
    # city_list = []
    city_list = city_dict['2']

    threads = []

    "Ilceleri threadlere dagitiyor. ilce basina 1 thread."
    for elem in interests:
        for i, county in enumerate(city_list):
            t = myThread(a, elem, county, i, 'istanbul')
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
            result = t.venues
            for venue in result:
                if '"' not in venue['venue_name']:
                    sql_string = sql.SQL(
                        "INSERT INTO venue (category_id, venue_id, venue_name, overall_rating, start_hour, end_hour, price, image_url, city)"
                        " VALUES ('{}', '{}', '{}', {}, '{}', '{}', {}, '{}', '{}')".format(
                            venue["category_id"],
                            venue["venue_id"],
                            venue["venue_name"].replace("'", '"'),
                            venue["venue_rating"],
                            venue["start_hour"],
                            venue["end_hour"],
                            venue["price"] if venue.get('price', None) else 0,
                            venue["image_url"],
                            "2"
                        ))
                    a.execute_insert(sql_string)


if __name__ == '__main__':
    venue_add()
