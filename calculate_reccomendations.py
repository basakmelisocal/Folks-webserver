#!/usr/bin/python
from sources.recommendation_manager.recommendation_helpers import calculate_venue_rating, \
    calculate_user_user_similarity, calculate_user_rating
from sources.data_manager.rel_db_manager import RelationalDBManager as DBManager

def main():
    database_access = DBManager()
    calculate_user_user_similarity(database_access)
    calculate_venue_rating(database_access)
    calculate_user_rating(database_access)


if __name__ == '__main__':
    main()