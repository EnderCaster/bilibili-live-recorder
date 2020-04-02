#!/usr/bin/env python3
import random
from Live import BiliBiliLive
import os
import sys
import requests
import time
import config
import utils
import re
import multiprocessing
import urllib3
urllib3.disable_warnings()


class BiliBiliLiveRecorder(BiliBiliLive):
    def __init__(self, room_id, check_interval=5*60):
        super().__init__(room_id)
        self.inform = utils.inform
        self.print = utils.print_log
        self.check_interval = check_interval
        self.informed=False

    def check(self, interval):
        while True:
            room_info = self.get_room_info()
            try:
                self.print(self.room_id,"scanning...")
                if room_info['status']:
                    if not self.informed:
                        self.inform(room_id=self.room_id,
                                    desp=room_info['roomname'],user=room_info['hostname'])
                        self.print(self.room_id, room_info['roomname'])
                        self.informed=True
                else:
                    self.informed=False
                    self.print(self.room_id, "Waiting for living")
            except Exception as e:
                self.print(self.room_id, 'Error:' + str(e))
            time.sleep(interval*(1+random.random()))

    def run(self):
        while True:
            self.check(interval=config.check_interval)


if __name__ == '__main__':
    input_id = config.rooms  # input_id = '917766' '1075'

    mp = multiprocessing.Process
    tasks = [mp(target=BiliBiliLiveRecorder(room_id).run)
             for room_id in input_id]
    for i in tasks:
        i.start()
    for i in tasks:
        i.join()
