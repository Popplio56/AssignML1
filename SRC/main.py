import cv2
import torch
from torch import load
import sys
import time

cap = cv2.VideoCapture(0)
frame_count = 0
prev_time = time.time()
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release() 
cv2.destroyAllWindows()