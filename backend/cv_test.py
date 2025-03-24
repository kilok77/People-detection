import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

plt.imshow(frame)

cap.release()