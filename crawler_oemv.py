from datetime import datetime
import urllib
import json
import time
import pprint
from helper.manage_json import load_dictionary_from_json, save_dictionary_to_json
from proxy.proxy_scraper import getFreeProxies
from helper.manage_omv_session import Omvpetrom
from helper.image_processing import ImageProcessing

class OEMV_Crawler():
    
    def __init__(self):
        
        self.JSON_PATH = "/Users/simon/python/gas_station_crawler/json/gas_stations_oemv.json"
        self.URL = "https://app.wigeogis.com/kunden/omvpetrom/data/details.php"
        self.STATION_LIST = load_dictionary_from_json(self.JSON_PATH)['results']
        self.SESSION_PARAMS = self.refresh_session()
        
        print("Total stations loaded: ", len(self.STATION_LIST))
        #print("Session parameters: ")
        #pprint.pprint(self.SESSION_PARAMS)

    def refresh_session(self):
        omv_session = Omvpetrom()
        return omv_session.get_session_params()

    def get_price_url(self, station_id):
        self.SESSION_PARAMS['ID'] = station_id
        data = urllib.parse.urlencode(self.SESSION_PARAMS).encode()
        raw = urllib.request.urlopen(self.URL, data=data,)
        jsonized = json.loads(raw.read().decode('utf-8'))
        return jsonized['priceUrl']

    def crawl(self):
        # get prices for all stations
        for station in self.STATION_LIST:
            
            # Only check Vienna stations
            if(station['town_l'] == 'Wien'):
                
                # get price for stations
                sid = station['sid']
                print("Processing: ", sid)
                price_url = self.get_price_url(sid)
                print("Price URL: ", price_url)
                processor = ImageProcessing(price_url)
                res = processor.process()
                pprint.pprint(res)
                break


o = OEMV_Crawler()
o.crawl()