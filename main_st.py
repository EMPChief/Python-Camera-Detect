import cv2
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="EMP Camera Test",
    page_icon="favicon.ico",
)
st.title("Motion Detector")
camera_index = st.number_input("Camera Index", value=0, step=1)
start_button = st.button('Start Camera')

if start_button:
    displayed_image = st.image([])
    camera = cv2.VideoCapture(camera_index)
    first_frame = None
    while True:
        success, frame = camera.read()
        if not success:
            st.error("Failed to capture frame!")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if first_frame is None:
            first_frame = gray
            continue
        frame_delta = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) < 10000:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        now = datetime.now()
        cv2.putText(img=frame, text=now.strftime("%A"), org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)
        
        cv2.putText(img=frame, text=now.strftime("%H:%M:%S"), org=(30, 140),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 0, 0),
                    thickness=2, lineType=cv2.LINE_AA)
        
        displayed_image.image(frame)
