import cv2
import time
from EmailSender import EmailSender
import datetime

CAMERA_NUMBER = 172
VIDEO_DEVICE_INDEX = 0
video_capture = cv2.VideoCapture(VIDEO_DEVICE_INDEX)
time.sleep(3)
previous_frame = None
status_list = []
while True:
    status = 0
    success, frame = video_capture.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if previous_frame is None:
        previous_frame = blurred_gray_frame
        continue

    delta_frame = cv2.absdiff(previous_frame, blurred_gray_frame)
    threshold_frame = cv2.threshold(delta_frame, 51, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(threshold_frame, None, iterations=3)
    contours, check = cv2.findContours(
        dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(
            frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[-0] == 1 and status_list[-1] == 0:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        EmailSender().send_email(f"Motion Detected {current_time}",
                                 f"Motion was detected on camera {CAMERA_NUMBER}", "support@empchief.com")
    font = cv2.FONT_HERSHEY_SIMPLEX
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, f"Camera {CAMERA_NUMBER} - {current_datetime}",
                (10, frame.shape[0] - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("Motion Detection", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
