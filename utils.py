import time
import requests
import config
import env_lang


def get_current_time(time_format):
    current_struct_time = time.localtime(time.time())
    current_time = time.strftime(time_format, current_struct_time)
    return current_time


def generate_filename(room_id):
    data = dict()
    data['c_time'] = get_current_time('%Y%m%d_%H%M')
    data['room_id'] = room_id
    return '_'.join(data.values()) + '.flv'


def inform(room_id, desp=''):
    if config.enable_inform:
        param = {
            'room_id': room_id,
            'room_title': desp,
        }
        resp = requests.get(url=config.inform_url, params=param)
        print(resp.content)
        print_log(room_id=room_id,
                  content='success') if resp.status_code == 200 else None
    else:
        pass


def print_log(room_id='None', content='None'):
    brackets = '[{}]'
    time_part = brackets.format(get_current_time('%Y-%m-%d %H:%M:%S'))
    room_part = brackets.format(env_lang.get('label.living_room') + room_id)
    print(time_part, room_part, content)


if __name__ == '__main__':
    print(generate_filename('1075'))
    print_log(content='开始录制')
