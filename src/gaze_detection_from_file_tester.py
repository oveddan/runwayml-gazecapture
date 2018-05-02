import cv2
from gaze_detector import extract_features_and_detect_gazes

img = cv2.imread('notebooks/photos/IMG-1035.JPG')

outputs = extract_features_and_detect_gazes(img)

print(outputs)
