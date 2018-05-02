import zmq
import sys
import threading
import time
from random import randint, random
import base64
import io
import numpy as np
from lib import current_time
from FaceAndEyeDetectorWorker import FaceAndEyeDetectorWorker

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5555')

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        image_receive_worker = ImageReceiveWorker(context)
        image_receive_worker.start()

        face_and_eye_detector_worker = FaceAndEyeDetectorWorker(image_receive_worker)

        face_and_eye_detector_worker.start()

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

class ImageReceiveWorker(threading.Thread):
    """ImageReceiveWorker"""
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context
        self.frame = None
        self.frame_time = None
        self.worker = None

    def run(self):
        self.worker = self.context.socket(zmq.DEALER)
        self.worker.connect('inproc://backend')
        self.worker.recv_string(flags=0)

        tprint('Worker started')
        while True:
            # md = worker.recv_string(flags=0)
            tprint('receiving')
            msg = self.worker.recv_json(flags=0)
            data = self.worker.recv(flags=0, copy=True, track=False)
            A = np.frombuffer(data, msg['dtype'])
            _=  self.worker.recv(flags=0, copy=True, track=False)

            self.frame = A.reshape(msg['shape'])
            tprint('received')
            self.frame_time = current_time()

            time.sleep(10)
            
            # print('got image with shape', self.frame.shape)

            
        self.worker.close()

    def read(self):
        return (self.frame, self.frame_time)

    def stop(self):
        if self.worker is not None:
            self.worker.close()
        
def main():
    """main function"""
    server = ServerTask()
    server.start()
    server.join()

if __name__ == "__main__":
    main()
