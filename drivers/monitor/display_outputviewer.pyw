import cv2

while True:
    img = cv2.imread('monitor_out.png')
    cv2.imshow('dst_rt', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()