from gaze_detector_from_camera_stream import GazeDetectorStream
import json
import socket
from WebcamVideoStream import WebcamVideoStream
from FaceAndEyeDetectorStream import FaceAndEyeDetectorStream 
from gaze import test_faces
from lib import current_time
from gaze_detector import extract_features_and_detect_gazes

vs = FaceAndEyeDetectorStream(0).start()

last_read = current_time()


for i=1:10
    #  print('Connected by', addr)
    while True:
        img, faces, face_features = vs.read()
        #  print(img.shape, faces, face_features)
        if img is not None:
            outputs = test_faces(img, faces, face_features)

            if len(outputs) > 0:
                print('time between frames', (current_time() - last_read) * 1. / 1000)
            last_read = current_time()
                    #  if not data: break
            # do whatever you need to do with the data
            
finally:
    vs.stop()
