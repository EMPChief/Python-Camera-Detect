import cv2
import time

# Video capture device selection:
# 0: webcam
# 1: external camera
# 2: external camera
VIDEO_DEVICE = 0
video_capture = cv2.VideoCapture(VIDEO_DEVICE)
time.sleep(3)

while True:
    success, frame = video_capture.read()
    print(f"Success: {success}")
    print(f"Frame: {frame}")
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
