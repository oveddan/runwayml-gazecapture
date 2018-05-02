from features import extract_image_features
from gaze import test_faces

def extract_features_and_detect_gazes(img):
    img, faces, face_features = extract_image_features(img)
    return test_faces(img, faces, face_features)
