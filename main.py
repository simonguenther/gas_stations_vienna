from crawler_avanti import Avanti_Crawler
from crawler_oemv import OEMV_Crawler

avanti = Avanti_Crawler()
oemv = OEMV_Crawler()

avanti.crawl()
oemv.crawl()