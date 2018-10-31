import cv2
import time
img1 = cv2.imread("test.jpg",0)
cv2.imshow("img1",img1)
cv2.moveWindow("img1", 100, 100)
cv2.waitKey(1000)
cv2.destroyWindow("img1")
img2 = cv2.imread("test.png",0)
cv2.imshow("img2",img2)
cv2.moveWindow("img2", 400, 100)
cv2.waitKey(1000)
cv2.destroyWindow("img2")
time.sleep(1)
img3 = cv2.imread("test.png",0)
cv2.imshow("img3",img2)
cv2.moveWindow("img3", 800, 100)
cv2.waitKey(1000)
cv2.destroyWindow("img3")

