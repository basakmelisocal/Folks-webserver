import threading
from recommendation_helpers import _venue_search, _get_ratings

class myThread(threading.Thread):
    def __init__(self, db_manager,user_category_array, cities, threadId, city_name):
        threading.Thread.__init__(self)
        self.db_manager = db_manager
        self.user_category_array = user_category_array
        self.cities = cities
        self.threadId = threadId
        self.city_name = city_name
        self.venues = list()

    def run(self):
        self.venues = _venue_search(self.db_manager, self.user_category_array, self.cities, self.city_name)

        "self.venues listindeki her venue icin _get_rating() fonksiyonunu ayri threadlerde cagiriyor."
        sizevenues = len(self.venues)
        threadnumber = sizevenues # WHAT IS THIS.

        if sizevenues % threadnumber == 0:
            size = sizevenues / threadnumber
            lastsize = size
        else:
            size = sizevenues / threadnumber
            last = sizevenues - (size * threadnumber)
            lastsize = size + last
        threadtemp = []

        for i in range(0, threadnumber):
            start = i * size
            end = (i + 1) * size
            if i == threadnumber - 1:
                start = i * size
                end = (i + 1) * lastsize
            t = myThread2(self.venues[start:end], i + 4)
            t.start()
            threadtemp.append(t)

        temp = list()
        for t in threadtemp:
            t.join()
            result = t.venues
            temp += result
        self.venues = temp


class myThread2(threading.Thread):
    def __init__(self, venues, threadId):
        threading.Thread.__init__(self)
        self.venues = venues
        self.threadId = threadId

    def run(self):
        self.venues = _get_ratings(self.venues)
