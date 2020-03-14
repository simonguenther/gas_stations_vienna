from datetime import datetime

def timestamp_log(transform = None):
    if(transform == None):
        return datetime.now().strftime('%d/%m/%Y %H:%M')
    else:
        try:
            _in = datetime.strptime(transform, '%d/%m/%Y %H:%M')
            return _in.strftime('%d/%m/%Y %H:%M')
        except:
            pass

        try:
            _in = datetime.strptime(transform, '%d %b %H:%M')
            return _in.strftime('%d/%m/%Y %H:%M')
        except:
            pass

def timestamp_file():
    return datetime.now().strftime('%Y_%m_%d_%H_%M')

