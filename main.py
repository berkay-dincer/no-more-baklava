import subprocess
import time
from ctypes import CDLL
import datetime

from FaceRecognizer import FaceRecognize


def get_readable_datetime():
    return datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")


def get_idle_time():
    io_stats = subprocess.Popen(["ioreg", "-c", "IOHIDSystem"], stdout=subprocess.PIPE)
    result = subprocess.Popen(["grep", "HIDIdleTime"], stdin=io_stats.stdout, stdout=subprocess.PIPE)

    io_stats.stdout.close()
    out, err = result.communicate()
    out = out.decode('utf-8')
    lines = out.split('\n')

    raw_line = ''
    for line in lines:
        if 'HIDIdleTime' in line:
            raw_line = line
            break

    nano_seconds = int(raw_line.split('=')[-1])
    seconds = nano_seconds / 10 ** 9
    return seconds


def lock_screen():
    CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login').SACLockScreenImmediate()


def main():
    recognizer = FaceRecognize()
    while True:
        time.sleep(2)
        current_idle_time = get_idle_time()
        print("{} - Baklava ping. Current idle time is: {}".format(get_readable_datetime(), current_idle_time))
        if current_idle_time > 20:
            if recognizer.is_face_present():
                print("{} - Detected a face. Locking computer, we will not eat baklava today..".format(
                    get_readable_datetime()))
                lock_screen()
                recognizer.close_camera()
                break


if __name__ == '__main__':
    main()
