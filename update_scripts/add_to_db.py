from sources.foursquare_api_connector import foursquare_connector
from sources.data_manager import rel_db_manager
from sources.account_manager.reg_oper import RegistrationOperations
from psycopg2 import sql
import random
import datetime

a = rel_db_manager.RelationalDBManager()
b = foursquare_connector.FoursquareConnector()

ArrayOfNames = [
    "Chayndunth, Lord Of The Brown",
    "Gayzzur, The White",
    "Bimroi, The Taker Of Life",
    "Qonnu, The Dead",
    "Churso, The Fast One",
    "Baethe, The Bunny Killer",
    "Chuvoa, The Protective",
    "Ovnanoal, The Protective",
    "Dunneintei, The Grumpy",
    "Peorlirrath, The Bright",
    "Dundeonth, The Squeeler",
    "Sedath, The Redeemer",
    "Zeovae, The Barbarian",
    "Deirma, Champion Of The Brown",
    "Golryr, The Victorious",
    "Cygiorth, Lord Of Ice",
    "Dundit, Destroyer Of Life",
    "Quvurriet, The Strong Minded",
    "Aezzyrun, Champion Of The Skies",
    "Eoludoalth, Protector Of The Forest",
    "Ilrie, The Puny",
    "Ziassut, The Calm",
    "Qeidraylth, Braveheart",
    "Diarleith, Giver Of Life",
    "Eige, The Fierce",
    "Fryzzoal, The Rabbit Slayer",
    "Todruss, The Grumpy",
    "Zeovniassaet, The Strong",
    "Arsonieth, The Hungry",
    "Qayveiral, The Evil One",
    "Ierrath, Eater Of All",
    "Naylass, Lord Of The White",
    "Oldrun, The Jealous One",
    "Xeiphael, The Dark One",
    "Tiolraylth, The Firestarter",
    "Vizyth, Champion Of The Green",
    "Uzzog, The Tall",
    "Nandrunioss, The Eternal",
    "Sunnoidurth, Champion Of The Skies",
    "Moanoarroanth, The Dark",
    "Caghad, The Clean",
    "Rayghianth, The Puny",
    "Tiallienth, The White One",
    "Aevraynth, The Kind",
    "Mayllerth, The Gifted",
    "Sumath, The Taker Of Life",
    "Ova, Lord Of The Black",
    "Qurmuryt, Redeemer Of Men",
    "Xuziedait, The Brave",
    "Pemorriolth, The Creep"
]
array_of_addresses = [
    "663 East Hilltop Road Webster, NY 14580",
    "690 Highland St. Garden City, NY 11530",
    "36 Central Ave. Pueblo, CO 81001",
    "544 Halifax Ave. Amityville, NY 11701",
    "653 Sunnyslope Road Erlanger, KY 41018",
    "876 Harvey Dr. Fremont, OH 43420",
    "21 Longfellow Ave.Kansas City, MO 64151",
    "7975 Spruce Road Danbury, CT 06810",
    "414 Pulaski St. Hyde Park, MA 02136",
    "8800 Acacia Street Lake Zurich, IL 60047",
    "39 Manor Dr. Evanston, IL 60201",
    "304 Ryan Drive Lansdowne, PA 19050",
    "4 Briarwood Street Palos Verdes Peninsula, CA 90274",
    "8165 Buttonwood St. Mount Holly, NJ 08060",
    "9057 Brewery Lane Staunton, VA 24401",
    "7355 Mayfield Ave. Irwin, PA 15642",
    "9 South Cherry Hill Street East Elmhurst, NY 11369",
    "15 Wild Rose Dr. Florence, SC 29501",
    "7288 Sheffield St. Stow, OH 44224",
    "375 Arcadia St. Cranberry Twp, PA 16066",
    "895 Brickyard Court Reisterstown, MD 21136",
    "626 Tarkiln Hill Lane Buckeye, AZ 85326",
    "9437 Ryan Rd. Elkhart, IN 46514",
    "461 Central Court Brockton, MA 02301",
    "27 Cedar Lane Waltham, MA 02453",
    "55 Bohemia St. Goshen, IN 46526",
    "900 Oakwood Street Algonquin, IL 60102",
    "88 Beacon St. Roselle, IL 60172",
    "754 Cooper Drive Loxahatchee, FL 33470",
    "7754 Cedarwood Ave. Coram, NY 11727",
    "8813 Clark Court Lake Mary, FL 32746",
    "29 Cherry Hill Court Sacramento, CA 95820",
    "375 Tunnel Dr. Livingston, NJ 07039",
    "9015 Buttonwood Court Coram, NY 11727",
    "799 Elizabeth Drive Parlin, NJ 08859",
    "79 Old York Ave. Largo, FL 33771",
    "451 Cedar St. Benton Harbor, MI 49022",
    "9612 Bridle Lane Peachtree City, GA 30269",
    "8 Belmont St. Hopkinsville, KY 42240",
    "7 Arnold Ave. Merrillville, IN 46410",
    "956 SW. Oklahoma St. Howard Beach, NY 11414",
    "35 Miles Avenue Mableton, GA 30126",
    "85 North Overlook Dr. Raeford, NC 28376",
    "727 Orange Drive El Paso, TX 79930",
    "76 Golf Dr. El Paso, TX 79930",
    "9261 Myrtle Lane Eden Prairie, MN 55347",
    "36 Morris Street Murrells Inlet, SC 29576",
    "9069 Plymouth St.Randallstown, MD 21133",
    "28 Taylor Lane Enfield, CT 06082",
    "54 Rocky River St. Goose Creek, SC 29445"
]
array_of_occupations = [
    "Computer Scientist",
    "Software Engineer",
    "Software Developer",
    "Architect",
    "Electical Engineer",
    "Mechanical Engineer",
    "Civil Engineer",
    "Doctor",
    "Nurse",
    "Lawyer",
    "Tour Guide",
    "Economist",
    "Student",
    "Teacher",
    "Professor"
]

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


def insert_interests(reldb, fs):
    category_dict = {
        'Entertainment': [
            '4fceea171983d5d06c3e9823',
            '4bf58dd8d48988d1e1931735',
            '4bf58dd8d48988d1e4931735',
            '4bf58dd8d48988d17c941735',
            '52e81612bcbc57f1066b79e7',
            '4bf58dd8d48988d18e941735',
            '52e81612bcbc57f1066b79e8',
            '4bf58dd8d48988d1f1931735',
            '52e81612bcbc57f1066b79ea',
            '5744ccdfe4b0c0459246b4bb',
            '52e81612bcbc57f1066b79e6',
            '52e81612bcbc57f1066b79eb',
            '4bf58dd8d48988d192941735',
            '4bf58dd8d48988d1e3931735',
            '56aa371be4b08b9a8d573514',
            '4bf58dd8d48988d1f4931735',
            '52e81612bcbc57f1066b79e9',
            '4bf58dd8d48988d182941735',
            '5109983191d435c0d71c2bb1',
            '4bf58dd8d48988d193941735',
            '4bf58dd8d48988d17b941735',
            '58daa1558bbb0b01f18ec1fd',
            '4bf58dd8d48988d119941735',
            '4bf58dd8d48988d120941735',
            '5032829591d4c4b30a586d5e',
            '5744ccdfe4b0c0459246b4b8',
            '52e81612bcbc57f1066b7a11',
        ],
        'Arts': [
            '4bf58dd8d48988d1e2931735',
            '56aa371be4b08b9a8d573532',
            '4bf58dd8d48988d18f941735',
            '4bf58dd8d48988d1f2931735',
            '507c8c4091d498d9fc8c67a9',
            '52e81612bcbc57f1066b79ed',
            '52e81612bcbc57f1066b79ee',
            '4bf58dd8d48988d199941735',
        ],
        'Theater': [
            '56aa371be4b08b9a8d5734db',
            '4bf58dd8d48988d137941735',
            '4bf58dd8d48988d1ac941735',
        ],
        'Cinema': [
            '4bf58dd8d48988d135941735',
            '4bf58dd8d48988d17f941735',
            '4bf58dd8d48988d17e941735',
            '56aa371be4b08b9a8d5734de',
            '4bf58dd8d48988d180941735'],
        'Opera': ['4bf58dd8d48988d136941735'],
        'Books': [
            '4bf58dd8d48988d1a7941735',
            '4bf58dd8d48988d12f941735',
            '4bf58dd8d48988d114951735',
            '4bf58dd8d48988d1b1941735',
            '52f2ab2ebcbc57f1066b8b30'
        ],
        'History': [
            '4bf58dd8d48988d190941735',
            '4deefb944765f83613cdba6e',
            '56aa371be4b08b9a8d5734db',
            '50aaa49e4b90af0d42d5de11',
            '52e81612bcbc57f1066b7a14',
            '5642206c498e4bfca532186c',
        ],
        'Sanctuary': [
            '52e81612bcbc57f1066b7a3e',
            '4bf58dd8d48988d132941735',
            '56aa371be4b08b9a8d5734fc',
            '52e81612bcbc57f1066b7a3f',
            '52e81612bcbc57f1066b7a40',
            '4bf58dd8d48988d138941735',
            '4eb1d80a4b900d56c88a45ff',
            '4bf58dd8d48988d139941735',
            '4bf58dd8d48988d13a941735',
            '56aa371be4b08b9a8d5734f6',
        ],
        'Landmark': ['4bf58dd8d48988d12d941735'],
        'Museum': [
            '4bf58dd8d48988d181941735',
            '4bf58dd8d48988d18f941735',
            '4bf58dd8d48988d190941735',
            '4bf58dd8d48988d192941735',
            '4bf58dd8d48988d191941735',
        ],
        'Music': [
            '4bf58dd8d48988d1e5931735',
            '4bf58dd8d48988d1e7931735',
            '4bf58dd8d48988d1e8931735',
            '4bf58dd8d48988d1e9931735',
            '5267e4d9e4b0ec79466e48d1',
            '4bf58dd8d48988d1fe941735',
        ],
        'Festival': [
            '5267e4d9e4b0ec79466e48c7',
            '5267e4d9e4b0ec79466e48d1',
            '52741d85e4b0d5d1e3c6a6d9',
        ],
        'Nightlife': [
            '4d4b7105d754a06376d81259',
            '4bf58dd8d48988d121941735',
            '4bf58dd8d48988d11f941735',
        ],
        'Bars': [
            '4bf58dd8d48988d116941735',
            '56aa371ce4b08b9a8d57356c',
            '52e81612bcbc57f1066b7a0e',
            '4bf58dd8d48988d11e941735',
            '4bf58dd8d48988d118941735',
            '4bf58dd8d48988d11b941735',
            '4bf58dd8d48988d11c941735',
            '4bf58dd8d48988d1d4941735',
            '4bf58dd8d48988d11d941735',
            '56aa371be4b08b9a8d57354d',
            '4bf58dd8d48988d122941735',
            '4bf58dd8d48988d123941735',
            '4bf58dd8d48988d155941735',
            '52e81612bcbc57f1066b7a06'],
        'Athletics': [
            '4bf58dd8d48988d184941735',
            '4bf58dd8d48988d18c941735',
            '4bf58dd8d48988d18b941735',
            '4bf58dd8d48988d18a941735',
            '4bf58dd8d48988d189941735',
            '4bf58dd8d48988d185941735',
            '56aa371be4b08b9a8d573556',
            '4bf58dd8d48988d188941735',
            '4e39a891bd410d7aed40cbc2',
            '4bf58dd8d48988d187941735',
            '4f4528bc4b90abdf24c9de85',
            '52e81612bcbc57f1066b7a2b',
            '4bf58dd8d48988d1e8941735',
            '4bf58dd8d48988d1e1941735',
            '52e81612bcbc57f1066b7a2f',
            '56aa371be4b08b9a8d57351a',
            '4bf58dd8d48988d1e6941735',
            '58daa1558bbb0b01f18ec1b0',
            '4bf58dd8d48988d175941735',
            '52f2ab2ebcbc57f1066b8b47',
            '503289d391d4c4b30a586d6a',
            '52f2ab2ebcbc57f1066b8b49',
            '4bf58dd8d48988d105941735',
            '52f2ab2ebcbc57f1066b8b48',
            '4bf58dd8d48988d176941735',
            '4bf58dd8d48988d101941735',
            '58daa1558bbb0b01f18ec203',
            '5744ccdfe4b0c0459246b4b2',
            '4bf58dd8d48988d106941735',
            '590a0744340a5803fd8508c3',
            '4bf58dd8d48988d102941735',
            '4cce455aebf7b749d5e191f5',
            '52e81612bcbc57f1066b7a2e',
            '52e81612bcbc57f1066b7a2d',
            '4e39a956bd410d7aed40cbc3',
            '4eb1bf013b7b6f98df247e07',
            '52e81612bcbc57f1066b7a2c',
            '4f452cd44b9081a197eba860',
            '56aa371be4b08b9a8d57352c',
            '4bf58dd8d48988d167941735',
            '4bf58dd8d48988d168941735',
        ],
        'Wine': [
            '4bf58dd8d48988d14b941735',
            '4bf58dd8d48988d123941735',
            '4bf58dd8d48988d119951735',
            '4bf58dd8d48988d1de941735',
        ],
        'College': [
            '4d4b7105d754a06372d81259',
            '4bf58dd8d48988d198941735',
            '4bf58dd8d48988d199941735',
            '4bf58dd8d48988d19a941735',
            '4bf58dd8d48988d19e941735',
            '4bf58dd8d48988d19d941735',
            '4bf58dd8d48988d19c941735',
            '4bf58dd8d48988d19b941735',
            '4bf58dd8d48988d19f941735',
            '4bf58dd8d48988d197941735',
            '4bf58dd8d48988d1af941735',
            '4bf58dd8d48988d1b1941735',
            '4bf58dd8d48988d1a1941735',
            '4bf58dd8d48988d1a0941735',
            '4bf58dd8d48988d1b2941735',
            '4bf58dd8d48988d1a5941735',
            '4bf58dd8d48988d1a7941735',
            '4bf58dd8d48988d1aa941735',
            '4bf58dd8d48988d1a9941735',
            '4bf58dd8d48988d1a3941735',
            '4bf58dd8d48988d1b4941735',
            '4bf58dd8d48988d1bb941735',
            '4bf58dd8d48988d1ba941735',
            '4bf58dd8d48988d1b9941735',
            '4bf58dd8d48988d1b8941735',
            '4bf58dd8d48988d1b5941735',
            '4bf58dd8d48988d1b7941735',
            '4e39a9cebd410d7aed40cbc4',
            '4bf58dd8d48988d1b6941735',
            '4bf58dd8d48988d1ac941735',
            '4bf58dd8d48988d1a2941735',
            '4bf58dd8d48988d1b0941735',
            '4bf58dd8d48988d1a8941735',
            '4bf58dd8d48988d1a6941735',
            '4bf58dd8d48988d1b3941735',
            '4bf58dd8d48988d141941735',
            '4bf58dd8d48988d1ab941735',
            '4bf58dd8d48988d1ad941735',
            '4bf58dd8d48988d1ae941735',
        ],
        'AmericanFood': [
            '4bf58dd8d48988d14e941735',
            '4bf58dd8d48988d157941735',
            '4bf58dd8d48988d16c941735',
            '4bf58dd8d48988d16f941735',
            '4bf58dd8d48988d1cc941735',
            '4bf58dd8d48988d14c941735',
            '4d4ae6fc7a7b7dea34424761',
            '4bf58dd8d48988d1bf941735',
        ],
        'AsianFood': [
            '4bf58dd8d48988d142941735',
            '56aa371be4b08b9a8d573568',
            '52e81612bcbc57f1066b7a03',
            '4eb1bd1c3b7b55596b4a748f',
            '52e81612bcbc57f1066b79fb',
            '52af0bd33cf9994f4e043bdd',
            '4bf58dd8d48988d156941735',
            '4eb1d5724b900d56c88a45fe',
            '4bf58dd8d48988d1d1941735',
            '56aa371be4b08b9a8d57350e',
            '4bf58dd8d48988d149941735',
            '56aa371be4b08b9a8d573502',
            '52af39fb3cf9994f4e043be9',
            '4bf58dd8d48988d14a941735',
            '4bf58dd8d48988d145941735',
            '52af3a5e3cf9994f4e043bea',
            '52af3a723cf9994f4e043bec',
            '52af3a7c3cf9994f4e043bed',
            '58daa1558bbb0b01f18ec1d3',
            '52af3a673cf9994f4e043beb',
            '52af3a903cf9994f4e043bee',
            '4bf58dd8d48988d1f5931735',
            '52af3a9f3cf9994f4e043bef',
            '52af3aaa3cf9994f4e043bf0',
            '52af3ab53cf9994f4e043bf1',
            '52af3abe3cf9994f4e043bf2',
            '52af3ac83cf9994f4e043bf3',
            '52af3ad23cf9994f4e043bf4',
            '52af3add3cf9994f4e043bf5',
            '52af3af23cf9994f4e043bf7',
            '52af3ae63cf9994f4e043bf6',
            '52af3afc3cf9994f4e043bf8',
            '52af3b053cf9994f4e043bf9',
            '52af3b213cf9994f4e043bfa',
            '52af3b293cf9994f4e043bfb',
            '52af3b343cf9994f4e043bfc',
            '52af3b3b3cf9994f4e043bfd',
            '52af3b463cf9994f4e043bfe',
            '52af3b633cf9994f4e043c01',
            '52af3b513cf9994f4e043bff',
            '52af3b593cf9994f4e043c00',
            '52af3b6e3cf9994f4e043c02',
            '52af3b773cf9994f4e043c03',
            '52af3b813cf9994f4e043c04',
            '52af3b893cf9994f4e043c05',
            '52af3b913cf9994f4e043c06',
            '52af3b9a3cf9994f4e043c07',
            '52af3ba23cf9994f4e043c08',
            '4deefc054765f83613cdba6f',
            '52960eda3cf9994f4e043ac9',
            '52960eda3cf9994f4e043acb',
            '52960eda3cf9994f4e043aca',
            '52960eda3cf9994f4e043acc',
            '52960eda3cf9994f4e043ac7',
            '52960eda3cf9994f4e043ac8',
            '52960eda3cf9994f4e043ac5',
            '52960eda3cf9994f4e043ac6',
            '4bf58dd8d48988d111941735',
            '55a59bace4b013909087cb0c',
            '55a59bace4b013909087cb30',
            '55a59bace4b013909087cb21',
            '55a59bace4b013909087cb06',
            '55a59bace4b013909087cb1b',
            '55a59bace4b013909087cb1e',
            '55a59bace4b013909087cb18',
            '55a59bace4b013909087cb24',
            '55a59bace4b013909087cb15',
            '55a59bace4b013909087cb27',
            '55a59bace4b013909087cb12',
            '4bf58dd8d48988d1d2941735',
            '55a59bace4b013909087cb2d',
            '55a59a31e4b013909087cb00',
            '55a59af1e4b013909087cb03',
            '55a59bace4b013909087cb2a',
            '55a59bace4b013909087cb0f',
            '55a59bace4b013909087cb33',
            '55a59bace4b013909087cb09',
            '55a59bace4b013909087cb36',
            '4bf58dd8d48988d113941735',
            '56aa371be4b08b9a8d5734e4',
            '56aa371be4b08b9a8d5734f0',
            '56aa371be4b08b9a8d5734e7',
            '56aa371be4b08b9a8d5734ed',
            '56aa371be4b08b9a8d5734ea'
        ],
        'FrenchFood': [
            '4bf58dd8d48988d10c941735',
            '57558b36e4b065ecebd306b6',
            '57558b36e4b065ecebd306b8',
            '57558b36e4b065ecebd306bc',
            '57558b36e4b065ecebd306b0',
            '57558b36e4b065ecebd306c5',
            '57558b36e4b065ecebd306c0',
            '57558b36e4b065ecebd306cb',
            '57558b36e4b065ecebd306ce',
            '57558b36e4b065ecebd306d1',
            '57558b36e4b065ecebd306b4',
            '57558b36e4b065ecebd306b2',
            '57558b35e4b065ecebd306ad',
            '57558b36e4b065ecebd306d4',
            '57558b36e4b065ecebd306d7',
            '57558b36e4b065ecebd306da',
            '57558b36e4b065ecebd306ba'
        ],
        'GreekFood': [
            '4bf58dd8d48988d10e941735',
            '53d6c1b0e4b02351e88a83e8',
            '53d6c1b0e4b02351e88a83e2',
            '53d6c1b0e4b02351e88a83d8',
            '53d6c1b0e4b02351e88a83d6',
            '53d6c1b0e4b02351e88a83e6',
            '53d6c1b0e4b02351e88a83e4',
            '53d6c1b0e4b02351e88a83da',
            '53d6c1b0e4b02351e88a83d4',
            '53d6c1b0e4b02351e88a83dc',
            '53d6c1b0e4b02351e88a83e0',
            '52e81612bcbc57f1066b79f3',
            '53d6c1b0e4b02351e88a83d2',
            '53d6c1b0e4b02351e88a83de'
        ],
        'IndianFood': [
            '4bf58dd8d48988d10f941735',
            '54135bf5e4b08f3d2429dfe5',
            '54135bf5e4b08f3d2429dff3',
            '54135bf5e4b08f3d2429dff5',
            '54135bf5e4b08f3d2429dfe2',
            '54135bf5e4b08f3d2429dff2',
            '54135bf5e4b08f3d2429dfe1',
            '54135bf5e4b08f3d2429dfe3',
            '54135bf5e4b08f3d2429dfe8',
            '54135bf5e4b08f3d2429dfe9',
            '54135bf5e4b08f3d2429dfe6',
            '54135bf5e4b08f3d2429dfdf',
            '54135bf5e4b08f3d2429dfe4',
            '54135bf5e4b08f3d2429dfe7',
            '54135bf5e4b08f3d2429dfea',
            '54135bf5e4b08f3d2429dfeb',
            '54135bf5e4b08f3d2429dfed',
            '54135bf5e4b08f3d2429dfee',
            '54135bf5e4b08f3d2429dff4',
            '54135bf5e4b08f3d2429dfe0',
            '54135bf5e4b08f3d2429dfdd',
            '54135bf5e4b08f3d2429dff6',
            '54135bf5e4b08f3d2429dfef',
            '54135bf5e4b08f3d2429dff0',
            '54135bf5e4b08f3d2429dff1',
            '54135bf5e4b08f3d2429dfde',
            '54135bf5e4b08f3d2429dfec',
            '52e81612bcbc57f1066b79f8',
        ],
        'ItalianFood': [
            '4bf58dd8d48988d110941735',
            '55a5a1ebe4b013909087cbb6',
            '55a5a1ebe4b013909087cb7c',
            '55a5a1ebe4b013909087cba7',
            '55a5a1ebe4b013909087cba1',
            '55a5a1ebe4b013909087cba4',
            '55a5a1ebe4b013909087cb95',
            '55a5a1ebe4b013909087cb89',
            '55a5a1ebe4b013909087cb9b',
            '55a5a1ebe4b013909087cb98',
            '55a5a1ebe4b013909087cbbf',
            '55a5a1ebe4b013909087cb79',
            '55a5a1ebe4b013909087cbb0',
            '55a5a1ebe4b013909087cbb3',
            '55a5a1ebe4b013909087cb74',
            '55a5a1ebe4b013909087cbaa',
            '55a5a1ebe4b013909087cb83',
            '55a5a1ebe4b013909087cb8c',
            '55a5a1ebe4b013909087cb92',
            '55a5a1ebe4b013909087cb8f',
            '55a5a1ebe4b013909087cb86',
            '55a5a1ebe4b013909087cbb9',
            '55a5a1ebe4b013909087cb7f',
            '55a5a1ebe4b013909087cbbc',
            '55a5a1ebe4b013909087cb9e',
            '55a5a1ebe4b013909087cbc2',
            '55a5a1ebe4b013909087cbad',
            '4bf58dd8d48988d1ca941735'

        ],
        'MexicanFood': [
            '4bf58dd8d48988d1c1941735',
            '58daa1558bbb0b01f18ec1d9',
            '4bf58dd8d48988d153941735',
            '4bf58dd8d48988d151941735',
            '56aa371ae4b08b9a8d5734ba',
            '5744ccdfe4b0c0459246b4d3'
        ],
        'MiddleEasternFood': [
            '4bf58dd8d48988d115941735',
            '56aa371be4b08b9a8d573529',
            '5744ccdfe4b0c0459246b4ca',
            '58daa1558bbb0b01f18ec1cd',
            '52e81612bcbc57f1066b79f7',
            '58daa1558bbb0b01f18ec1bc',
            '58daa1558bbb0b01f18ec1c0',
            '58daa1558bbb0b01f18ec1c4',
            '58daa1558bbb0b01f18ec1c7',
            '5744ccdfe4b0c0459246b4a8',
            '52e81612bcbc57f1066b79ff',
            '4bf58dd8d48988d10b941735',
            '5283c7b4e4b094cb91ec88d7'
        ],
        'Seafood': ['4bf58dd8d48988d1ce941735'],
        'TurkishFood': [
            '4f04af1f2fb6e1c99f3db0bb',
            '530faca9bcbc57f1066bc2f3',
            '530faca9bcbc57f1066bc2f4',
            '5283c7b4e4b094cb91ec88d8',
            '5283c7b4e4b094cb91ec88d9',
            '5283c7b4e4b094cb91ec88db',
            '5283c7b4e4b094cb91ec88d6',
            '56aa371be4b08b9a8d573535',
            '56aa371be4b08b9a8d5734bd',
            '5283c7b4e4b094cb91ec88d5',
            '5283c7b4e4b094cb91ec88da',
            '530faca9bcbc57f1066bc2f2',
            '58daa1558bbb0b01f18ec1df',
            '58daa1558bbb0b01f18ec1dc',
            '56aa371be4b08b9a8d5734bf',
            '56aa371be4b08b9a8d5734c1',
            '5283c7b4e4b094cb91ec88d4',
            '58daa1558bbb0b01f18ec1e2'],
        'BakeryDeserts': [
            '4bf58dd8d48988d16a941735',
            '4bf58dd8d48988d1d0941735',
            '4bf58dd8d48988d1bc941735',
            '512e7cae91d4cbb4e5efe0af',
            '4bf58dd8d48988d1c9941735',
            '5744ccdfe4b0c0459246b4e2',
            '52e81612bcbc57f1066b7a0a',
        ],
        'BreakfastSpot': ['4bf58dd8d48988d143941735'],
        'Cafe': ['4bf58dd8d48988d16d941735', '4bf58dd8d48988d128941735'],
        'CoffeeShop': ['4bf58dd8d48988d1e0931735', '56aa371be4b08b9a8d5734c1'],
        'VegetarianVeganFood': ['4bf58dd8d48988d1d3941735'],
        'Gluten_freeFood': ['4c2cd86ed066bed06c3c5209'],
        'OutdoorsRecreation': [
            '52e81612bcbc57f1066b7a22',
            '4bf58dd8d48988d1df941735',
            '4bf58dd8d48988d1e4941735',
            '56aa371be4b08b9a8d57353b',
            '56aa371be4b08b9a8d573562',
            '56aa371be4b08b9a8d573511',
            '4bf58dd8d48988d15b941735',
            '52e81612bcbc57f1066b7a23',
            '56aa371be4b08b9a8d573547',
            '4bf58dd8d48988d15a941735',
            '4bf58dd8d48988d1e0941735',
            '4bf58dd8d48988d160941735',
            '50aaa4314b90af0d42d5de10',
            '4bf58dd8d48988d161941735',
            '4bf58dd8d48988d15d941735',
            '55a5a1ebe4b013909087cb77',
            '4eb1d4d54b900d56c88a45fc',
            '52e81612bcbc57f1066b7a21',
            '52e81612bcbc57f1066b7a13',
            '4bf58dd8d48988d162941735',
            '4bf58dd8d48988d163941735',
            '56aa371be4b08b9a8d573541',
            '4eb1d4dd4b900d56c88a45fd',
            '50328a4b91d4c4b30a586d6b',
            '4bf58dd8d48988d165941735',
            '4bf58dd8d48988d166941735',
            '58daa1558bbb0b01f18ec1b9',
            '4eb1baf03b7b2c5b1d4306ca',
            '52e81612bcbc57f1066b7a10',
            '4bf58dd8d48988d159941735',
            '52e81612bcbc57f1066b7a24',
            '4bf58dd8d48988d1de941735',
            '5032848691d4c4b30a586d61',
            '56aa371be4b08b9a8d573560',
            '56aa371be4b08b9a8d5734c3',
            '4fbc1be21983fc883593e321',
            '4d4b7105d754a06377d81259',
            '56aa371be4b08b9a8d57355e'
        ],

    }
    own_cat = {}
    for index, elem in enumerate(category_dict.keys()):
        stringsql = sql.SQL("INSERT INTO interests (id,name) VALUES ('{}','{}')".format(index, elem.encode('utf-8')))
        db = rel_db_manager.RelationalDBManager()
        db.execute_insert(stringsql)
        own_cat.update({elem: index})

    inter = b.get_venue_categories()
    for elem in inter:
        # stringsql = sql.SQL("
        #     INSERT INTO interests (id,name) VALUES ('{}','{}')
        # ".format(elem['id'], elem['name'].encode('utf-8')))
        # db = rel_db_manager.RelationalDBManager()
        # db.execute_insert(stringsql)

        for key in category_dict:
            if elem['id'] in category_dict[key]:
                parent_sql = sql.SQL("INSERT INTO interests_parent_interest_rel (parentid, interestid) VALUES ('{}','{}')".format(own_cat[key], elem['id']))
                db = rel_db_manager.RelationalDBManager()
                db.execute_insert(parent_sql)


def dummy_data_initial():
    with open("dummy_data.txt", "r") as f:
        content = f.readlines()
    humans = list()
    for line in content:
        name_index = random.randint(0, 49)
        occup_index = random.randint(0, 15)
        line_data = line.replace("'", "")
        human = {
            'age': '',  # TODO calculate birthdate
            'city': line_data[1],
            'interests': line_data[2].replace('\r\n', '').split(','),
            'firstname': ArrayOfNames[name_index].split(',')[0],
            'surname': ArrayOfNames[name_index].split(',')[1],
            'email': "email{}@email.com".format(content.index(line)),
            'occupation': array_of_occupations[occup_index],
        }
        humans.append(human)
    print humans


def dummy_data_with_actual_data():
    sql_string = sql.SQL(
        "INSERT INTO userdb (firstname, surname, profile_picture_link, short_bio, home_city_id, email, pwd)VALUES ('Selin', 'Fildis', '', '', '1','selinfildis@gmail.com', '{}')".format(RegistrationOperations.encrypt_pwd("123")))
    a.execute_insert(sql_string)
    get_user_sql = sql.SQL("SELECT userid FROM userdb WHERE email='{}' AND pwd='{}'".format('selinfildis@gmail.com', RegistrationOperations.encrypt_pwd("123")))
    id = a.execute_command(get_user_sql)[0][0]
    # Parsing user checkins to certain categories
    with open('nyc.txt', 'r') as f:
        data_from_file = f.read()
    data_from_file = data_from_file.split('\n')
    data = list()
    for elem in data_from_file:
        data.append(elem)

    checkin_list = list()
    unique_uid_dict = dict()
    print 1
    for checkin in data:
        splitted = checkin.split('\t')
        if splitted and splitted[0] and splitted[2] and splitted[3]:
            checkin_dict = {
                "user_id": splitted[0],
                "category_id": splitted[2],
                "category_name": splitted[3],
            }
            checkin_list.append(checkin_dict)
        if checkin_dict['user_id'] not in unique_uid_dict.keys():
            unique_uid_dict.update({checkin_dict['user_id']: ''})
    print 2
    for index, user in enumerate(unique_uid_dict.keys()):
        # creating and adding users :)))
        name_index = random.randint(0, 49)
        occup_index = random.randint(0, 14)
        year = random.randint(1930, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        city = random.randint(1, 7)
        gender = random.randint(0, 1)
        human = {
            'bdate': datetime.date(year, month, day).strftime("%d-%m-%y"),
            'city_id': city,
            'firstname': ArrayOfNames[name_index].split(',')[0],
            'surname': ArrayOfNames[name_index].split(',')[1],
            'email': "email{}@email.com".format(index),
            'occupation': array_of_occupations[occup_index],
            'home_city_id': city,
            'gender': 'Male' if gender == 0 else 'Female',
            'password': RegistrationOperations.encrypt_pwd(str(index))
        }
        user_sql = sql.SQL("INSERT INTO userdb(firstname, surname, birthdate, occupation, gender, email, pwd, home_city_id)VALUES ('{}','{}','{}','{}','{}','{}','{}', '{}') ".format(human['firstname'],
                   human['surname'],
                   human['bdate'],
                   human['occupation'],
                   human['gender'],
                   human['email'],
                   human['password'],
                   human['home_city_id']
                   ))

        a.execute_insert(user_sql)
        get_user_sql = sql.SQL("SELECT userid FROM userdb WHERE email='{}' AND pwd='{}'".format(human['email'], human['password']))
        uid = a.execute_command(get_user_sql)[0][0]
        arr = [0 for _ in range(0, 33)]
        unique_uid_dict[user] = uid
        checkin_vect = sql.SQL(
            "INSERT INTO user_checkin_rel(user_id, checkin_count) VALUES ({}, ARRAY [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] )".format(
                uid, arr))
        a.execute_insert(checkin_vect)
        if index % 100 == 0:
            sql_string = sql.SQL("INSERT INTO contacts(local_id, visitor_id) VALUES('{}','{}')".format(id,unique_uid_dict[user]))
            a.execute_insert(sql_string)


    print 3
    for element in checkin_list:
        parent_interest_sql = sql.SQL("SELECT parentid from interests_parent_interest_rel WHERE interestid='{}'".format(element['category_id']))
        result = a.execute_command(parent_interest_sql)
        if result:
            parent_id = result[0][0]
            update_checkin_vector_sql = sql.SQL("UPDATE user_checkin_rel SET checkin_count[{}+1]=checkin_count[{}+1] + 1 WHERE user_id={}".format(parent_id, parent_id, unique_uid_dict[element['user_id']]))

            a.execute_insert(update_checkin_vector_sql)
    print 4
    for user in unique_uid_dict.keys():
        sql_for_getting_interests = sql.SQL(" SELECT checkin_count FROM user_checkin_rel WHERE user_id={}".format(unique_uid_dict[user]))
        res = a.execute_command(sql_for_getting_interests)
        # finding max 3:
        max1 = 0
        max1_index = -1
        max2 = 0
        max2_index = -1
        max3 = 0
        max3_index = -1
        print res
        for element in res[0][0]:
            if element > max1:
                print max1
                max1 = element
                max1_index = res[0][0].index(element)

        for element in res[0][0]:
            if element > max2 and max1_index != res[0][0].index(element):
                print max2
                max2 = element
                max2_index = res[0][0].index(element)

        for element in res[0][0]:
            if element > max3 and max1_index != res[0][0].index(element) and max2_index != res[0][0].index(element):
                print max3
                max3 = element
                max3_index = res[0][0].index(element)

        interests_array = []
        interests_array.append(max1_index)
        interests_array.append(max2_index)
        interests_array.append(max3_index)
        for elem in interests_array:
            print interests_array
            if elem != -1:
                sql_string = sql.SQL("INSERT INTO user_interest_rel(userid, interestid) VALUES ({}, {})".format(unique_uid_dict[user], elem))
                a.execute_insert(sql_string)
        # Add dummy user, connect some of these people who are from a different city. (DEMO USER)


if __name__ == '__main__':
    dummy_data_with_actual_data()
