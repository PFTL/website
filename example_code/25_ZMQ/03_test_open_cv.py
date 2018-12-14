import cv2
import numpy as np
import matplotlib.pyplot as plt


cap = cv2.VideoCapture(0)

ret, frame = cap.read()
cap.release()

print(np.min(frame))
print(np.max(frame))

plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.show()