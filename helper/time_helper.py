from datetime import datetime

def timestamp_log(transform = None):
    if(transform == None):
        return datetime.now().strftime('%d/%m/%Y %H:%M')
    else:
        _in = datetime.strptime(transform, '%d/%m/%Y %H:%M')
        return _in.strftime('%d/%m/%Y %H:%M')

def timestamp_file():
    return datetime.now().strftime('%Y_%m_%d_%H_%M')

