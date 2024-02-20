import cv2
import time
from EmailSender import EmailSender

VIDEO_DEVICE_INDEX = 0
video_capture = cv2.VideoCapture(VIDEO_DEVICE_INDEX)
time.sleep(3)
previous_frame = None

while True:
    success, frame = video_capture.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if previous_frame is None:
        previous_frame = blurred_gray_frame
        continue

    delta_frame = cv2.absdiff(previous_frame, blurred_gray_frame)
    threshold_frame = cv2.threshold(delta_frame, 51, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(threshold_frame, None, iterations=3)
    contours, check = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Motion Detection", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

EmailSender().send_email("Motion Detected", "Motion was detected in the video stream.", "support@empchief.com")
