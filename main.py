from crawler_avanti import Avanti_Crawler
from crawler_oemv import OEMV_Crawler
from crawler_aral import Aral_Crawler
from crawler_shell import Shell_Crawler
import schedule
import time


"""
    TODO
    - implement central logging
    - use proxy for init session at avanti and ömv
    - generalize global variables 
"""

avanti = Avanti_Crawler()
oemv = OEMV_Crawler()
aral = Aral_Crawler()
shell = Shell_Crawler()

def job():
    print("I'm working...")

    shell.crawl()
    aral.crawl()
    avanti.crawl()
    oemv.crawl()

schedule.every(30).minutes.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
