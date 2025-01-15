import cv2 
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    a,img = cap.read()
    cv2.imwrite("name1.jpg",img)
    break
cap.release()