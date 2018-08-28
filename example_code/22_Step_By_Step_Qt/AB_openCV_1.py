import cv2
import numpy as np


cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

print(np.min(frame))
print(np.max(frame))