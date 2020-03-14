from crawler_avanti import Avanti_Crawler
from crawler_oemv import OEMV_Crawler

"""
    TODO
    - implement central logging
    - use proxy for init session at avanti and ömv
    
"""

avanti = Avanti_Crawler()
oemv = OEMV_Crawler()

#avanti.crawl()
#oemv.crawl()