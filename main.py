from FaceRecognizer import FaceRecognize
import argparse


def main(mode, image_count, name):
    recognizer = FaceRecognize()
    if mode == 'train':
        recognizer.capture_images(name=name, image_count=image_count)
        recognizer.train()
    else:
        print(recognizer.infer())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add some integers.')
    parser.add_argument('mode', type=str, help='mode of execution - train, no-more-baklava')
    parser.add_argument('count', type=int, default=10, help='number of pictures to take for training session.')
    parser.add_argument('name', type=str, help='name of the person in picture.')
    args = parser.parse_args()
    main(args.mode, args.count, args.name)
