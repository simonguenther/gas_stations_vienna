from crawler_avanti import Avanti_Crawler
from crawler_oemv import OEMV_Crawler
from crawler_aral import Aral_Crawler

"""
    TODO
    - implement central logging
    - use proxy for init session at avanti and ömv
    - generalize global variables 
"""

#avanti = Avanti_Crawler()
#oemv = OEMV_Crawler()
aral = Aral_Crawler()

aral.crawl()

#avanti.crawl()
#oemv.crawl()