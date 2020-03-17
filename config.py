import sys,os
import time, datetime

PWD = os.path.realpath('.')

OUTPUT_DIR = PWD+"/data/"
ERROR_DIR = PWD+"/error/"
TMP_DIR = PWD+"/tmp/"
JSON_DIR = PWD+"/json/"

def create_datetime_directory():
    today = datetime.date.today()  
    todaystr = today.isoformat()   
    path = PWD+"/data/"+todaystr+"/"
    print("Creating Directory: ", path)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    if os.path.exists(path):
        print("Setting OUTPUT_DIR to: ", path)
        global OUTPUT_DIR
        OUTPUT_DIR = path


