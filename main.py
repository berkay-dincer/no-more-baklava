import datetime

from FaceRecognizer import FaceRecognize
from OsHandler import OsHandler


def get_readable_datetime():
    return datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S")


def main():
    recognizer = FaceRecognize()
    os_handler = OsHandler()
    flow(os_handler, recognizer)


def flow(os_handler, recognizer):
    current_idle_time = os_handler.get_idle_time()
    if os_handler.is_screen_locked():
        print("{} - Computer is locked, we are safe.".format(get_readable_datetime()))
    print("{} - Baklava ping. Current idle time is: {}".format(get_readable_datetime(), current_idle_time))
    if current_idle_time > 10:
        if recognizer.is_face_present():
            print("{} - Detected a face. Locking computer, we will not eat baklava today..".format(
                get_readable_datetime()))
            recognizer.close_camera()
            os_handler.lock_screen()


if __name__ == '__main__':
    main()
