import time
import requests
import config
import hashlib


def get_current_time(time_format):
    current_struct_time = time.localtime(time.time())
    current_time = time.strftime(time_format, current_struct_time)
    return current_time


def inform(room_id, desp='',user=''):
    if config.enable_inform:
        p_hash= hashlib.md5(("{},{},{},{}".format(room_id,desp,user,config.inform_sign)).encode("utf8")).hexdigest()
        param = {
            'room_id': room_id,
            'room_title': desp,
            'user_name':user,
            'sign':p_hash
        }
        resp = requests.get(url=config.inform_url, params=param)
        print_log(room_id=room_id,
                  content=resp.text) if resp.status_code == 200 else None
    else:
        pass


def print_log(room_id='None', content='None'):
    brackets = '[{}]'
    time_part = brackets.format(get_current_time('%Y-%m-%d %H:%M:%S'))
    room_part = brackets.format("living room: {}".format(room_id))
    print(time_part, room_part, content)
