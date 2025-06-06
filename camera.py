import cv2
click=cv2.VideoCapture(0)
while True:
    status,photo=click.read()
    cv2.imshow("Camera",photo)
    if cv2.waitKey(10)==13:
        cv2.destroyAllWindows()
       click.release()
       break