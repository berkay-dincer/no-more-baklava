import os
import time
import datetime
from OsHandler import OsHandler


def get_readable_datetime():
    return datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S")


while True:
    time.sleep(2)
    os_handler = OsHandler()

    current_idle_time = os_handler.get_idle_time()
    print("{} - Baklava ping. Current idle time is: {}".format(get_readable_datetime(), current_idle_time))
    if current_idle_time <= 20:
        continue

    if os_handler.is_screen_locked():
        print("{} - Computer is locked, we are safe.".format(get_readable_datetime()))
        continue

    os.system('python3 main.py')
