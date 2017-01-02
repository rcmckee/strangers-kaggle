import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

def segment(dataset, subdir, name):
    img = cv2.imread(subdir + name)
    if not os.path.exists(subdir + 'step0/'):
        os.makedirs(subdir + 'step0/')
    # print(img.dtype)
    # print(img[10,10,:])
    b,g,r = cv2.split(img)
    # print(b[10,:])
    if b.item(10,10) is not 1:
        print(b.item(10,10))
    cv2.imwrite(subdir + 'step0/' + name[:-4] + 'b.tif', b)
    cv2.imwrite(subdir + 'step0/' + name[:-4] + 'g.tif', g)
    cv2.imwrite(subdir + 'step0/' + name[:-4] + 'r.tif', r)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    retval, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # while(True):
    gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
    thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 1)

    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
        kernel, iterations=4)

    cont_img = closing.copy()
    # contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    _, contours, _ = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 2000 or area > 4000:
            continue

        if len(cnt) < 5:
            continue

        ellipse = cv2.fitEllipse(cnt)
        cv2.ellipse(roi, ellipse, (0,255,0), 2)

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
