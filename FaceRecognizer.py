import pickle
import signal
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from skimage.transform import resize
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC


class FaceRecognize(object):
    def __init__(self):
        self.vc = None
        self.cascade = cv2.CascadeClassifier('model/haarcascade_frontalface_alt2.xml')
        self.margin = 10
        self.batch_size = 1
        self.is_interrupted = False
        self.data = {}
        self.le = None
        self.clf = None
        self.model = load_model('model/facenet_keras.h5')

    def _prewhiten(self, x):
        if x.ndim == 4:
            axis = (1, 2, 3)
            size = x[0].size
        elif x.ndim == 3:
            axis = (0, 1, 2)
            size = x.size
        else:
            raise ValueError('Dimension should be 3 or 4')

        mean = np.mean(x, axis=axis, keepdims=True)
        std = np.std(x, axis=axis, keepdims=True)
        std_adj = np.maximum(std, 1.0 / np.sqrt(size))
        y = (x - mean) / std_adj
        return y

    def _l2_normalize(self, x, axis=-1, epsilon=1e-10):
        output = x / np.sqrt(np.maximum(np.sum(np.square(x), axis=axis, keepdims=True), epsilon))
        return output

    def _calc_embs(self, imgs, margin, batch_size):
        aligned_images = self._prewhiten(imgs)
        pd = []
        for start in range(0, len(aligned_images), batch_size):
            pd.append(self.model.predict_on_batch(aligned_images[start:start + batch_size]))
        embs = self._l2_normalize(np.concatenate(pd))

        return embs

    def _signal_handler(self, signal, frame):
        self.is_interrupted = True

    def _load_training_pickles(self):
        pickle_dir = 'owner_images/'
        pickles = os.listdir(pickle_dir)
        all_data = dict()
        for p in pickles:
            pickle_in = open(pickle_dir + "/" + p, "rb")
            face_data = pickle.load(pickle_in)
            all_data = {**all_data, **face_data}
        self.data = all_data

    def capture_images(self, image_count, name='Unknown'):
        vc = cv2.VideoCapture(0)
        self.vc = vc
        if vc.isOpened():
            is_capturing, _ = vc.read()
        else:
            is_capturing = False

        imgs = []
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
                face = faces[0]
                (x, y, w, h) = face
                left = x - self.margin // 2
                right = x + w + self.margin // 2
                bottom = y - self.margin // 2
                top = y + h + self.margin // 2
                img = resize(frame[bottom:top, left:right, :],
                             (160, 160), mode='reflect')
                imgs.append(img)
                cv2.rectangle(frame,
                              (left - 1, bottom - 1),
                              (right + 1, top + 1),
                              (255, 0, 0), thickness=2)

            plt.imshow(frame)
            plt.title('{}/{}'.format(len(imgs), image_count))
            plt.xticks([])
            plt.yticks([])
            if len(imgs) == image_count:
                vc.release()
                self.data[name] = np.array(imgs)
                pickle_out = open("owner_images/" + name + ".pickle", "wb")
                pickle.dump(self.data, pickle_out)
                pickle_out.close()
                break
            try:
                plt.pause(0.1)
            except Exception:
                pass
            if self.is_interrupted:
                vc.release()
                break

    def train(self):
        self._load_training_pickles()
        labels = []
        embs = []
        self._load_training_pickles()
        names = self.data.keys()
        for name, imgs in self.data.items():
            embs_ = self._calc_embs(imgs, self.margin, self.batch_size)
            labels.extend([name] * len(embs_))
            embs.append(embs_)

        embs = np.concatenate(embs)
        le = LabelEncoder().fit(labels)
        y = le.transform(labels)
        clf = SVC(kernel='linear', probability=True).fit(embs, y)

        self.le = le
        self.clf = clf
        pickle_le = open("le.pickle", "wb")
        pickle.dump(le, pickle_le)
        pickle_le.close()

        pickle_clf = open("clf.pickle", "wb")
        pickle.dump(clf, pickle_clf)
        pickle_clf.close()

    def infer(self):
        pickle_le = open("le.pickle", "rb")
        self.le = pickle.load(pickle_le)

        pickle_clf = open("clf.pickle", "rb")
        self.clf = pickle.load(pickle_clf)

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
            pred = None
            if len(faces) != 0:
                face = faces[0]
                (x, y, w, h) = face
                left = x - self.margin // 2
                right = x + w + self.margin // 2
                bottom = y - self.margin // 2
                top = y + h + self.margin // 2
                img = resize(frame[bottom:top, left:right, :],
                             (160, 160), mode='reflect')
                embs = self._calc_embs(img[np.newaxis], self.margin, 1)
                pred = self.le.inverse_transform(self.clf.predict(embs))
                cv2.rectangle(frame,
                              (left - 1, bottom - 1),
                              (right + 1, top + 1),
                              (255, 0, 0), thickness=2)
            plt.imshow(frame)
            plt.title(pred)
            plt.xticks([])
            plt.yticks([])
            try:
                plt.pause(0.1)
            except Exception:
                pass
            if self.is_interrupted:
                vc.release()
                break
            return pred
