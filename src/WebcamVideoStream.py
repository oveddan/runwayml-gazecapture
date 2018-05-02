# import the necessary packages
from threading import Thread
from lib import current_time 
import cv2

class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        cap = cv2.VideoCapture(src)
        cap.set(3,1280)
        cap.set(4,720)
        self.stream = cap

        (self.grabbed, self.frame) = self.stream.read()
        self.frame_time = current_time()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            #  print('updating')
            if self.stopped:
                #  print('returning')
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            self.frame_time = current_time()
            #  print('updated', self.grabbed)

    def read(self):
        # return the frame most recently read
        return (self.frame, self.frame_time)

    def stop(self):
        # indicate that the thread should be stopped
        self.stream.release()
        self.stopped = True
