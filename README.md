# Presence

Presence is a kinetic sculpture that detects a viewer's gaze in real-time using a convolutional neural-network and moves in response to the gaze

It uses a webcam and the pre-trained model from [Eye Tracking for Everyone](http://gazecapture.csail.mit.edu/) to detect
where users are gazing, and moves in the direction of the gaze.

## Key files/documentation

**Full documentation coming soon**

* http://www.danioved.com/blog/posts/presence/ - blog posts which document the process 
* [The jupyter notebook](https://github.com/oveddan/presence/blob/master/notebooks/Predicting%20Gaze%20with%20Eye%20Tracking%20for%20Everyone.ipynb) that walks through how features are extracted in opencv and fed through the neural network to obtain a gaze prediction.
* [features.py](/features.py) - the code to extract features from input images using opencv
* [gaze.py](/gaze.py) - the code to feed the features through the pre-trained neural network and get a gaze prediction
* [processing_sketches/GazeFromStream3d](/processing_sketches/GazeFromStream3d) - processing sketch to render a simulation of the columns in 3d, and send servo positions over serial to the kinetic sculpture.

## Requirements

For gaze detection:

* python
* caffe
* opencv

To render simulations of the servo positions:

* processing
