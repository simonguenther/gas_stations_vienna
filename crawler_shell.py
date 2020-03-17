from bs4 import BeautifulSoup
import requests
import json
import time
import pprint
import config
from helper.manage_json import load_dictionary_from_json, save_dictionary_to_json
from helper.time_helper import timestamp_file, timestamp_log

class Shell_Crawler():

    def __init__(self):
        self.JSON_PATH = config.JSON_DIR+"gas_stations_shell.json"
        self.OUTPUT_DIR = config.OUTPUT_DIR
        self.STATION_LIST = load_dictionary_from_json(self.JSON_PATH)
        self.CRAWLER_NAME = "SHELL"
        self.USE_PROXY_FOR_CRAWLING = False
        print("Total stations loaded: ", len(self.STATION_LIST))


    """
    #
    # Get Price Page Source from Gas Station URL
    #
    """
    def get_price_page_from_station_url(self,station_url):
        source = requests.get(station_url)
        return BeautifulSoup(source.text, "html.parser")

    """
    #
    # Extract Price info from price page source
    #
    """
    def extract_price_from_source(self, source):

        gas_prices = source.findAll('div',{"class":"fuels__row"})
        gas_price_dict = {}
        
        for price_block in gas_prices:
                price_text = price_block.find("span",{"class":"fuels__row-type"})
                price_price = price_block.find("span",{"class":"fuels__row-price"})
                if(price_text is not None):
                    price_text = price_text.text.lower()
                    gas_price_dict[price_text] = price_price.text.strip('€').strip('/Ltr').replace('.',',')
                else:
                    timestamp = source.find('span', {"class":"fuels__row-updated"})
                    if(timestamp is not None):
                        gas_price_dict["timestamp"] = timestamp_log(timestamp.text[14:].strip())
                        
        #pprint.pprint(gas_price_dict)
        return gas_price_dict

    def save_pricefeed(self, feed):
        filename = self.OUTPUT_DIR+"{}___{}.json".format(self.CRAWLER_NAME, timestamp_file())
        save_dictionary_to_json(feed,filename)

    def crawl(self):
        data = {}
        for x in self.STATION_LIST:
            if(x['state'] == 'Wien'):
                print("Analyzing: " + x['id'])
                price_page_raw = self.get_price_page_from_station_url(x['website_url'])
                data[x['id']] = self.extract_price_from_source(price_page_raw)
        self.save_pricefeed(data)