import cv2
import streamlit as st
from datetime import datetime

st.title("Motion Detector")
start_button = st.button('Start Camera')

if start_button:
    displayed_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            st.error("Failed to capture frame!")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        now = datetime.now()
        
        cv2.putText(img=frame, text=now.strftime("%A"), org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)
        
        cv2.putText(img=frame, text=now.strftime("%H:%M:%S"), org=(30, 140),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 0, 0),
                    thickness=2, lineType=cv2.LINE_AA)
        
        displayed_image.image(frame)
