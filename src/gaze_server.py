from gaze_detector_from_camera_stream import GazeDetectorStream
import json
import socket
from FaceAndEyeDetectorStream import FaceAndEyeDetectorStream 
from gaze import test_faces
from lib import current_time, smooth_outputs
from gaze_detector import extract_features_and_detect_gazes
import signal
import sys

def to_output_string(outputs):
    output_string = None
    if (len(outputs) > 0):
        output_string = ""
        for i, output in enumerate(outputs):
            if output is not None:
                output_string += str(output[0]) + ',' + str(output[1])

                if (i < len(outputs) - 1):
                    output_string += '_'
    #  print("output string", output_string)
    return output_string

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 4001 # Arbitrary non-privileged port
vs = FaceAndEyeDetectorStream(0).start()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

last_read = current_time()

set_to_gpu = False

previous_outputs = []
previous_frame_time = None

try:
    #  print('Connected by', addr)
    while True:
        img, faces, face_features, frame_time = vs.read()
        #  print(img.shape, faces, face_features)
        if img is not None:
            new_outputs = test_faces(img, faces, face_features)

            if len(new_outputs) > 0:
                outputs = smooth_outputs(new_outputs, frame_time, previous_outputs, previous_frame_time)
                #  print('original outputs', new_outputs)
                #  print('smoothed outputs', outputs)
                previous_outputs = outputs
                previous_frame_time = frame_time
                #  outputs.append([0, 0])
                #  outputs.append([1, 1])
                output_string = to_output_string(outputs)
                if output_string:
                    print('time since taken ', current_time() - frame_time)
                    conn.send((output_string + '\n').encode())

            last_read = current_time()
                    #  if not data: break
            # do whatever you need to do with the data
            
finally:
    vs.stop()
    conn.close()


def signal_handler(signal, frame):
    vs.stop()
    conn.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


