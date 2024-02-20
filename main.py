import cv2
import time
from EmailSender import EmailSender


VIDEO_DEVICE_INDEX = 0
# VIDEO_DEVICE_INDEX = int(input("Enter video device index: (0(webcam), 1(external camera), 2(external camera)): "))
video_capture = cv2.VideoCapture(VIDEO_DEVICE_INDEX)
time.sleep(3)
first_frame = None
while True:
    success, frame = video_capture.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    if first_frame is None:
        first_frame = blurred_gray_frame
        continue
    
    cv2.imshow("Video", blurred_gray_frame)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
EmailSender().send_email("Test Subject", "Test Body", "empchief@gmail.com")
