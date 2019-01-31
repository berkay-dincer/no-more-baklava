import signal
import datetime
import cv2


class FaceRecognize(object):
    def __init__(self):
        self.vc = None
        self.cascade = cv2.CascadeClassifier('model/haarcascade_frontalface_alt2.xml')
        self.margin = 10
        self.batch_size = 1
        self.is_interrupted = False
        self.data = {}

    def _signal_handler(self, signal, frame):
        self.is_interrupted = True

    def is_face_present(self):
        vc = cv2.VideoCapture(0)
        self.vc = vc
        if vc.isOpened():
            is_capturing, _ = vc.read()
        else:
            is_capturing = False

        signal.signal(signal.SIGINT, self._signal_handler)
        self.is_interrupted = False
        while is_capturing:
            is_capturing, frame = vc.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = self.cascade.detectMultiScale(frame,
                                                  scaleFactor=1.1,
                                                  minNeighbors=3,
                                                  minSize=(100, 100))
            if len(faces) != 0:
                current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                image_name = 'images/' + current_datetime + '.jpg'
                cv2.imwrite(image_name, frame)
                print("!!!! Saved image at {} find out who was trying to order baklava!".format(image_name))
                return True
            return False

    def close_camera(self):
        vc = cv2.VideoCapture(0)
        vc.release()
        cv2.destroyAllWindows()
        current_datetime = datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
        print('{} Closing camera.'.format(current_datetime))

