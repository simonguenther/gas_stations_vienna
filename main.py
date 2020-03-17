from crawler_avanti import Avanti_Crawler
from crawler_oemv import OEMV_Crawler
from crawler_aral import Aral_Crawler
from crawler_shell import Shell_Crawler
import config
import schedule
import time


"""
    TODO
    - implement central logging
    - use proxy for init session at avanti and ömv
    - generalize global variables 
"""


def job():
    print("I'm working...")

    shell.crawl()
    aral.crawl()
    avanti.crawl()
    oemv.crawl()

def update_directory():
    config.create_datetime_directory()

    print("OUTPUT_DIR: ", config.OUTPUT_DIR)
    print("ERROR_DIR: ", config.ERROR_DIR)
    print("TMP DIR: ", config.TMP_DIR)
    print("JSON_DIR: ", config.JSON_DIR)
    print("-"*30)


update_directory()
avanti = Avanti_Crawler()
oemv = OEMV_Crawler()
aral = Aral_Crawler()
shell = Shell_Crawler()
print("-"*30)

schedule.every(1).minutes.do(job)

#schedule.every().hour.do(job)
schedule.every().day.at("00:00").do(update_directory)

while 1:
    schedule.run_pending()
    time.sleep(1)
