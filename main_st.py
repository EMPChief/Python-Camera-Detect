import streamlit as st
import cv2
import time
import numpy as np
import datetime
st.set_page_config(
    page_title="EMP Camera Test",
    page_icon="favicon.ico",
)

st.title("Motion Detection Streamlit App")
st.sidebar.header("Settings")
camera_number = st.sidebar.number_input("Camera Number", value=172)
video_device_index = st.sidebar.number_input("Video Device Index", value=0)
threshold_value = st.sidebar.slider("Threshold Value", 0, 255, 51)
min_contour_area = st.sidebar.slider("Minimum Contour Area", 0, 50000, 10000)

start_button = st.sidebar.button("Start Camera")
video_capture = None
previous_frame = None
status_list = []

if start_button:
    video_capture = cv2.VideoCapture(video_device_index)
    time.sleep(3)

while video_capture is not None and video_capture.isOpened():
    status = 0
    success, frame = video_capture.read()
    if not success:
        st.error("Failed to capture frame!")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if previous_frame is None:
        previous_frame = blurred_gray_frame
        continue

    delta_frame = cv2.absdiff(previous_frame, blurred_gray_frame)
    threshold_frame = cv2.threshold(delta_frame, threshold_value, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(threshold_frame, None, iterations=3)
    contours, _ = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < min_contour_area:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        status = 1
    
    status_list.append(status)
    status_list = status_list[-2:]
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, f"Camera {camera_number} - {current_datetime}",
                (10, frame.shape[0] - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    st.image(frame_rgb, channels="RGB", use_column_width=True)
    st.markdown("Press 'q' to quit")

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

if video_capture is not None:
    video_capture.release()

