from FaceAndEyeDetectorStream import FaceAndEyeDetectorStream 
from gaze import test_faces
from lib import current_time, smooth_outputs
from gaze_detector import extract_features_and_detect_gazes
import warnings
warnings.filterwarnings("ignore")


vs = FaceAndEyeDetectorStream(0).start()

last_read = current_time()

set_to_gpu = False

previous_outputs = []
previous_frame_time = None

try:
    while True:
        img, faces, face_features, frame_time = vs.read()
        #  print(img.shape, faces, face_features)
        if img is not None:
            new_outputs = test_faces(img, faces, face_features)

            if len(new_outputs) > 0:
                outputs = smooth_outputs(new_outputs, frame_time, previous_outputs, previous_frame_time)
                print('original outputs', new_outputs)
                print('smoothed outputs', outputs)
                previous_outputs = outputs
                previous_frame_time = frame_time

            #  if len(outputs) > 0:
                #  print('time between frames', (current_time() - last_read) * 1. / 1000)
                #  print('time since frame', (current_time() - frame_time) * 1. / 1000)
            last_read = current_time()
                    #  if not data: break
            # do whatever you need to do with the data
            
finally:
    vs.stop()
