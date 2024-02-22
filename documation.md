# Motion Detector Documentation

## Overview
This script `motion_detector.py` is designed to detect motion using a webcam or video device connected to the computer. It continuously captures frames from the camera, processes them to detect motion, and performs actions such as saving images when motion is detected and sending an email notification. It utilizes the OpenCV library for image processing and an `EmailSender` class for sending emails.

## Dependencies
- `cv2` (OpenCV): Used for video capture, image processing, and motion detection.
- `time`: Used for introducing delays.
- `EmailSender`: Custom class for sending email notifications.
- `datetime`: Used for timestamping and formatting date and time.
- `glob`: Used for file path manipulation.

## Classes and Methods

### MotionDetector
- `__init__(self, camera_id=173, video_device_index=0)`: Initializes the Motion Detector with optional parameters for camera ID and video device index.
    - Attributes:
        - `camera_id`: The ID of the camera.
        - `video_device_index`: Index of the video device.
        - `previous_frame`: Stores the previous frame for motion comparison.
        - `status_list`: List to keep track of motion status.
        - `count`: Counter for the number of motion events.
- `start_capture()`: Begins capturing frames from the video device and processes them for motion detection.
- `detect_motion(blurred_gray_frame, frame)`: Performs motion detection on the provided frame.
    - Parameters:
        - `blurred_gray_frame`: Blurred and converted grayscale version of the frame.
        - `frame`: Original color frame from the camera.
    - Process:
        - Compares the current frame with the previous frame to detect motion.
        - Draws rectangles around detected motion areas.
        - Saves images when motion is detected.
        - Updates `status_list` to check for consecutive motion status changes.
        - Calls `send_motion_email()` when motion status changes from detected to not detected.
        - Calls `display_text(frame)` to add camera ID and timestamp to the frame.
        - Displays the processed frame with motion detection.
- `send_motion_email()`: Sends an email notification when motion is detected.
- `display_text(frame)`: Adds camera ID and current datetime to the frame for display.

### EmailSender
- `send_email(subject, body, to_email)`: Sends an email with specified subject, body, and recipient.

## Usage
To use the Motion Detector:

1. Import the necessary libraries:
```python
import cv2
import time
from EmailSender import EmailSender
import datetime
import glob
```
