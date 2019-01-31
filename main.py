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
    while True:
        if recognizer.is_face_present():
            print("{} - Detected a face. Locking computer, we will not eat baklava today..".format(
                get_readable_datetime()))
            recognizer.close_camera()
            os_handler.lock_screen()
            break


if __name__ == '__main__':
    main()
