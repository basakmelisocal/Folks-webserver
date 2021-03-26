import json
import foursquare

class FoursquareConnector:
    client_id = 'W1ZKOE4C2MDLZS2UITNYY5RNHTRGMSPLQBB5MQAE4RZ2AKIO'
    client_secret = 'A4100OK512W0JSDNIQ5MBU5MKQ0KMFJMNQED4AES14Z4JRI4'
    to_delete_from_any_venue = ['beenHere', 'venueChains', 'hereNow',
                                'allowMenuUrlEdit', 'hasPerk']

    to_delete_from_category = ['pluralName', 'shortName', 'icon']

    def __init__(self):
        self.client = foursquare.Foursquare(client_id=self.client_id,
                                            client_secret=self.client_secret)

    def get_venue_details(self, venue_id):
        resp = self.client.venues(venue_id)
        return resp

    def search_venues(self,params):
        resp = self.client.venues.search(params=params)
        del resp['geocode']

        for venue in resp['venues']:
            for key in venue.keys():
                if key in self.to_delete_from_any_venue:
                    del venue[key]
        
        return resp

    def get_venue_categories(self):
        resp = self.client.venues.categories()
        resp = self._category_parser(resp)
        return self._category_linearizer(resp)

    def venue_tips(self, venue_id):
        return self.client.venues.tips(venue_id)

    def similar_venues(self, venue_id):
        return self.client.venues.similar(venue_id)

    def _category_parser(self, resp):
        for category in resp['categories']:
            for key in category.keys():
                if key in self.to_delete_from_category:
                    del category[key]
                if key == 'categories' and category[key]:
                    self._category_parser(category)
        return resp

    def _category_linearizer(self, req):
        resp = list()
        for category in req['categories']:
            resp.append({'id': category['id'], 'name': category['name']})
            if category['categories']:
                resp.extend(self._category_linearizer(category))
        return resp
