import requests
import urllib
import pprint
import re
import random
from bs4 import BeautifulSoup
import sys

class getFreeProxies():
    def __init__(self, url= "https://free-proxy-list.net/uk-proxy.html"):
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
        self.timeout_seconds = 10
        self.FREE_PROXIES = url
        self.raw = self.get_raw_from_url(self.FREE_PROXIES)
        self.proxies = self.scrape_website(self.raw)
        print("Proxies scraped: ", len(self.proxies))

    # Get random proxy o_O
    def get_random_proxy(self):
        rnd = random.choice(self.proxies)
        while(self.proxy_is_working(rnd) == False):
            rnd = random.choice(self.proxies)
        return rnd
    
    # Get Sourcecode from URL, optional with proxy (as dictionary 'protocol':'ip:port')
    def get_raw_from_url(self, url, proxies=None):
        print("Proxy status: ", proxies)
        if proxies == None:
            return requests.get(url,headers=self.headers).text
        else:
            try:
                print("Running request with proxy")
                return requests.get(url,timeout= self.timeout_seconds, headers=self.headers,proxies=proxies).text
            except NameError as ne:
                print("Exception raised: ", ne)
            except:
                print(sys.exc_info()[0])
                
        return False

    # Scrape anonymous proxy list 
    def scrape_website(self, code):
        soup = BeautifulSoup(code, 'html.parser')
        proxy_entry = soup.find_all("tr")#, {"class":"odd"})
        _proxies = []
        for row in proxy_entry:
            single = row.find_all("td")
            if(len(single) == 8):

                if(single[4].text == "anonymous"):
                    # return format: dictionary
                    # 'http(s):'ip:port''
                    # to use it as proxies dict 
                    # with request later on
                    key = 'https' if (single[6].text == "yes") else 'http'
                    value = single[0].text.strip()+":"+single[1].text.strip()
                    _proxies.append({key:value})
        return _proxies
    
    # Check if proxy is working
    def proxy_is_working(self, proxy):
        _url = "http://www.showmemyip.com/"
        _proxy = {}
        for k in proxy:
            _proxy[k] = "http://"+proxy[k]
        #proxy = {k:("http://{}".format(v)) for k,v in proxy}
        _source = self.get_raw_from_url(_url, _proxy)
        
        # Handle exceptions
        if(_source == False):
            print("Source returned nothing")
            return False
        
        _soup = BeautifulSoup(_source, 'html.parser')
        
        # Handle some connection problems/drops
        if _soup == None or _soup == False:
            print("_soup is empty")
            return False
        
        inputs = _soup.find("title")
    
        
        # Proxy not working
        if inputs == None: 
            return False 

        # Get returned IP from title tag
        response_ip = inputs.text.split()[-1]
        
        if(response_ip in list(proxy.values())[0]):
            print("proxy is working")
            return True
        return False
    
    # Get whole proxy dictionary
    def get_proxies(self):
        return self.proxies

