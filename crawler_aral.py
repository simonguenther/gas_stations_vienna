from bs4 import BeautifulSoup
import requests
import json
import time
import pprint
from helper.manage_json import load_dictionary_from_json, save_dictionary_to_json
from helper.time_helper import timestamp_file, timestamp_log


class Aral_Crawler():

    def __init__(self):
        self.JSON_PATH = "/Users/simon/python/gas_station_crawler/json/gas_stations_aral.json"
        self.PRICEFEED_URL = "https://bpatpricesfe.geoapp.me/v1/at/prices?bpc_txt_pricing_disclaimer=Ohne%20gewahr%20-%20es%20geiten%20de%20Preise%20an%20der%20Zapfsaule&bpc_txt_pricing_na=Preise%20zur%20Zeit%20nicht%20verf%C3%BCgbar&bpc_txt_pricing_stand=Stand&project=navitas&branding=bp&location_id="
        self.OUTPUT_DIR = "/Users/simon/python/gas_station_crawler/data/"
        self.STATION_LIST = load_dictionary_from_json(self.JSON_PATH)
        self.CRAWLER_NAME = "ARAL"
        self.USE_PROXY_FOR_CRAWLING = False
        print("Total stations loaded: ", len(self.STATION_LIST))

    """
    #
    # Get source of price page from station_id input
    #
    """
    def get_price_page_from_station_id(self, station_id):
        lookup_url = self.PRICEFEED_URL+station_id
        print("Fetching Price sourcecode")
        source = requests.get(lookup_url)
        return BeautifulSoup(source.text, "html.parser")

    """ 
    # 
    # Check if Price feed is available
    # 
    """
    def price_feed_available(self, price_page_source):
        if(price_page_source.find('p',{"class":"no-prices"}) == None):
            return True
        return False


    """
    #
    # Extract Price info from price page source
    #
    """
    def extract_price_from_source(self, source):
        timestamp = source.find('div',{"class":"timestamp"}).p.text.split()[:2]
        gas_prices = source.find('ul',{"class":"pricelist"}).findAll('li')
        gas_prices_dict = {}
        gas_prices_dict['timestamp'] = timestamp_log(" ".join(timestamp))
        for gas in gas_prices:
            price_text = gas.find('p',{"class":"price-text"}).text.lower().strip()
            price_price = gas.find('p',{"class":"price-value"}).text.strip('€').replace(",",".").strip()
            gas_prices_dict[price_text] = price_price
        return gas_prices_dict

    def save_pricefeed(self, feed):
        filename = self.OUTPUT_DIR+"{}___{}.json".format(self.CRAWLER_NAME, timestamp_file())
        save_dictionary_to_json(feed,filename)

    def crawl(self):
        data = {}
        for station in self.STATION_LIST:
            print("Getting prices for: ", station)
            price_page_raw = self.get_price_page_from_station_id(station)
            if(self.price_feed_available(price_page_raw)):
                        price_info = self.extract_price_from_source(price_page_raw)
                        #pprint.pprint(price_info)
                        data[station] = price_info
        
        self.save_pricefeed(data)
        