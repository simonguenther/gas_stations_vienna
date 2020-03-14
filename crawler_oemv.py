from datetime import datetime
import urllib
import json
import time
import pprint
from helper.manage_json import load_dictionary_from_json, save_dictionary_to_json
from proxy.proxy_scraper import getFreeProxies
from helper.manage_omv_session import Omvpetrom
from helper.image_processing import ImageProcessing
from helper.time_helper import timestamp_log, timestamp_file
#import helper.path_variables

"""
Todo:
 - implement logger module in all files
"""

class OEMV_Crawler():
    
    def __init__(self, verbose = False):
        
        #logging.basicConfig(filename='oemv_app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        self.JSON_PATH = "/Users/simon/python/gas_station_crawler/json/gas_stations_oemv.json"
        self.URL = "https://app.wigeogis.com/kunden/omvpetrom/data/details.php"
        self.OUTPUT_DIR = "/Users/simon/python/gas_station_crawler/data/"
        self.STATION_LIST = load_dictionary_from_json(self.JSON_PATH)['results']
        self.SESSION_PARAMS = self.refresh_session()
        self.CRAWLER_NAME = "OEMV"
        self.USE_PROXY_FOR_CRAWLING = False
        self.PICTURE_FORMAT = "png"
        
        #print("Session parameters: ")
        #pprint.pprint(self.SESSION_PARAMS)

    def refresh_session(self):
        omv_session = Omvpetrom()
        return omv_session.get_session_params()

    def get_price_url(self, station_id, proxy = None):
        self.SESSION_PARAMS['ID'] = station_id
        data = urllib.parse.urlencode(self.SESSION_PARAMS).encode()

        if(proxy == None):
            raw = urllib.request.urlopen(self.URL, data=data)
        else:
            ipport = list(proxy.values())[0]
            print("Using proxy for request: ", ipport)
            #create the object, assign it to a variable
            _proxy = urllib.request.ProxyHandler({'http': ipport})
            # construct a new opener using your proxy settings
            opener = urllib.request.build_opener(_proxy)
            # install the openen on the module-level
            urllib.request.install_opener(opener)
            # make a request
            raw = urllib.request.urlopen(self.URL, data=data)
        
        jsonized = json.loads(raw.read().decode('utf-8'))
        return jsonized['priceUrl']

    def extract_prices_all_station(self):
        
        # dictionary[station_id] = dict of prices
        all_prices = {}
        if(self.USE_PROXY_FOR_CRAWLING):
            p = getFreeProxies()
            proxy_wport = p.get_random_proxy()

        # get prices for all stations
        for station in self.STATION_LIST:
            
            # Only check Vienna stations
            if(station['town_l'] == 'Wien'):
                
                # get price for stations
                sid = station['sid']

                print("-"*40)
                print("Processing: ", sid)
                if(self.USE_PROXY_FOR_CRAWLING):
                    price_url = self.get_price_url(sid, proxy_wport)
                else:
                    price_url = self.get_price_url(sid)
                print("Price URL: ", price_url)

                # Extract Price Info From Image
                processor = ImageProcessing(price_url)
                res = processor.process()

                all_prices[sid] = res
        return all_prices

    def save_pricefeed(self, feed):
        filename = self.OUTPUT_DIR+"{}___{}.json".format(self.CRAWLER_NAME, timestamp_file())
        save_dictionary_to_json(feed,filename)

    def crawl(self):
        pricefeed = self.extract_prices_all_station()
        self.save_pricefeed(pricefeed)

