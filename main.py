import cv2
import time
from EmailSender import EmailSender
import datetime
import glob

class MotionDetector:
    def __init__(self, camera_id=173, video_device_index=0):
        self.camera_id = camera_id
        self.video_device_index = video_device_index
        self.previous_frame = None
        self.status_list = []
        self.count = 0

    def start_capture(self):
        video_capture = cv2.VideoCapture(self.video_device_index)
        time.sleep(3)

        try:
            while True:
                motion_detected = 0
                success, frame = video_capture.read()
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blurred_gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

                self.detect_motion(blurred_gray_frame, frame)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

        except Exception as e:
            print("An error occurred:", str(e))

        finally:
            video_capture.release()
            cv2.destroyAllWindows()

    def detect_motion(self, blurred_gray_frame, frame):
        if self.previous_frame is None:
            self.previous_frame = blurred_gray_frame
            return

        delta_frame = cv2.absdiff(self.previous_frame, blurred_gray_frame)
        threshold_frame = cv2.threshold(
            delta_frame, 51, 255, cv2.THRESH_BINARY)[1]
        dilated_frame = cv2.dilate(threshold_frame, None, iterations=3)
        contours, _ = cv2.findContours(
            dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 10000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(
                frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            motion_detected = 1
            cv2.imwrite(
                f"image/motion_detected_{self.camera_id}_{self.count}.png", frame)
            self.count += 1
            all_image = glob.glob("image/motion_detected_*")

        self.status_list.append(motion_detected)
        self.status_list = self.status_list[-2:]
        if self.status_list[-2] == 1 and self.status_list[-1] == 0:
            self.send_motion_email()

        self.display_text(frame)

        cv2.imshow("Motion Detection", frame)

    def send_motion_email(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        EmailSender().send_email(f"Motion Detected {current_time}",
                                 f"Motion was detected on camera {self.camera_id}", "support@empchief.com")

    def display_text(self, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, f"Camera {self.camera_id} - {current_datetime}",
                    (10, frame.shape[0] - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

if __name__ == "__main__":
    MotionDetector().start_capture()
