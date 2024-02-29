import cv2
import streamlit as st
from datetime import datetime

def set_page_config():
    st.set_page_config(
        page_title="EMP Camera Test",
        page_icon="favicon.ico",
    )

def display_title():
    st.title("Motion Detector")

def get_camera_index():
    return st.number_input("Camera Index", value=0, step=1)

def start_camera(camera_index):
    camera = cv2.VideoCapture(camera_index)
    first_frame = None
    image_placeholder = st.empty()
    return camera, first_frame, image_placeholder

def capture_frame(camera):
    success, frame = camera.read()
    if not success:
        st.error("Failed to capture frame!")
        return None
    return frame

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    return gray

def detect_motion(first_frame, current_frame):
    frame_delta = cv2.absdiff(first_frame, current_frame)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_rectangles(frame, contours):
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame

def display_frame(image_placeholder, frame):
    image_placeholder.image(frame)

def main():
    set_page_config()
    display_title()
    camera_index = get_camera_index()
    camera, first_frame, image_placeholder = start_camera(camera_index)

    while True:
        frame = capture_frame(camera)
        if frame is None:
            break
        current_frame = process_frame(frame)
        if first_frame is None:
            first_frame = current_frame
            continue
        contours = detect_motion(first_frame, current_frame)
        frame = draw_rectangles(frame, contours)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        now = datetime.now()
        cv2.putText(img=frame, text=now.strftime("%A"), org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=now.strftime("%H:%M:%S"), org=(30, 140),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 0, 0),
                    thickness=2, lineType=cv2.LINE_AA)
        display_frame(image_placeholder, frame)
        first_frame = current_frame

if __name__ == "__main__":
    main()
