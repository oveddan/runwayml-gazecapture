from WebcamVideoStream import WebcamVideoStream
from features import extract_image_features, draw_detected_features
from lib import current_time
import numpy as np

import cv2

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

try:
    for i in range(1, 100):
        _, img = cap.read()
        #  print(img.shape, faces, face_features)
        if img is not None:
            print('writing frame', i)
            cv2.imwrite('output/frame-' + str(i) + '.png', img)
            img, faces, face_features = extract_image_features(img)
            images_with_features = np.copy(img)
            draw_detected_features(images_with_features, faces, face_features)
            cv2.imwrite('output/frame-' + str(i) + '-features.png', images_with_features )


            # do whatever you need to do with the data

finally:
    cap.release()
