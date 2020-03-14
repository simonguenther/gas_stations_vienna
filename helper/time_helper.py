from datetime import datetime

def timestamp_log():
    return datetime.now().strftime('%d/%m/%Y %H:%M')

def timestamp_file():
    return datetime.now().strftime('%Y_%m_%d_%H_%M')