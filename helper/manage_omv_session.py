import urllib
import random
from bs4 import BeautifulSoup

class Omvpetrom():

    def __init__(self):
        self.OMVPETROMURL = "https://app.wigeogis.com/kunden/omvpetrom/map.php"

    
    def get_request_parameters(self):
        __url = self.OMVPETROMURL
        # prep get parameters
        __get = {}
        __get['CTRISO'] = 'AUT'
        __get['LNG'] = 'DE'

        # construct full request URL
        get_values = urllib.parse.urlencode(__get)
        full = __url+'?'+get_values

        # fire request and decode return
        data = urllib.request.urlopen(full)
        content = data.read().decode("utf-8")

        # extract IConfHash and IConfTs
        _soup = BeautifulSoup(content,'html.parser')

        js_tags = _soup.findAll('script',{'type':'text/javascript'})

        _params = {}
        
        for js in js_tags:
            if 'IConfHash' in js.text:
                hash_index = js.text.find('var IConfHash')
                commands = js.text[hash_index:].split(';')
                commands = [c.strip() for c in commands]
                for c in commands:
                    if 'IConfHash' in c:
                        _params['HASH'] = c.split('=')[1].replace("'","").strip()

                    if 'IConfTs' in c:
                        _params['TS'] = int(c.split('=')[1].replace("'","").strip())

        return _params


    # Construct Param Dictionary with station_id missing
    def get_session_params(self):
        params = self.get_request_parameters()
        if(len(params) > 0):
            #params['ID'] = station_id
            params['LNG'] = 'DE'
            params['CTRISO']= 'AUT'
            params['VEHICLE']='CAR'
            params['MODE']='NEXTDOOR'
            params['BRAND']='OMV'
            params['DISTANCE']=int(random.randrange(100,2000))
        else:
            print("so much empty")
        return params


