import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from pytesseract import image_to_string
import os
import sys
path = sys.path[0]
img_path = 'car_google4.jpeg'


def detect_plate(img_path):
    plate = cv2.CascadeClassifier(os.path.join(path,'static', 'cascades', 'data', 'haarcascade_russian_plate_number.xml'))

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # plates = plate.detectMultiScale(gray, 1.2, 4)
    plates = plate.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(4, 4))
    for (x, y, w, h) in plates:
        color = (22, 0, 255)
        stroke = 3
        cv2.rectangle(img, (x, y), (x + w + 5, y + h), color, stroke)

        try:
            croped_img = img[y:y + h, x:x + w + 5]
            return img, croped_img
        except:
            return img, img

        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def segment(image):
    H = 100.
    height, width, depth = image.shape
    imgScale = H / height
    newX, newY = image.shape[1] * imgScale, image.shape[0] * imgScale

    image = cv2.resize(image, (int(newX), int(newY)))
    cv2.imwrite("resizeimg.jpg", image)
    idx = 0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO)
    cv2.imwrite('static/new_final_plate_hue.jpg', thresh)
    """
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        idx += 1
        x, y, w, h = cv2.boundingRect(cnt)
        roi = image[y:y + h, x:x + w]
        if (w > 10 and h > 15):
            rs = make_white(roi)
    return rs"""


def make_white(nemo):
    light_white = (0, 0, 200)
    dark_white = (145, 60, 255)
    hsv_nemo = cv2.cvtColor(nemo, cv2.COLOR_RGB2HSV)
    mask_white = cv2.inRange(hsv_nemo, light_white, dark_white)
    result_white = cv2.bitwise_and(nemo, nemo, mask=mask_white)
    return result_white

def pic_ocr(final_plate_path):
    img=Image.open(final_plate_path)
    txt=image_to_string(img)
    return txt


def trace_plate(img_path):
    img_path = os.path.join(sys.path[0],'media', 'temp_objects', img_path)
    a=0
    #for img_sample, img in detect_plate(img_path):
    img, plate = detect_plate(img_path)
    segment(plate)
    cv2.imwrite('static/segment%s.jpg' % (str(a)), img)
    #cv2.imwrite('static/plate%s.jpg' % (str(a)), img_sample)
    #cv2.imwrite('static/new_final_plate_org.jpg', final_plate)
    #cv2.imwrite('static/new_final_plate.jpg', final_plate)
    #t1 = pic_ocr(os.path.join(path, 'static', 'new_final_plate.jpg'))
    t2 = pic_ocr(os.path.join(path, 'static', 'new_final_plate_hue.jpg'))
    #t3 = pic_ocr(os.path.join(path, 'static', 'new_final_plate_org.jpg'))
    print(t2,'some')
    return {'data_list': ['segment'+str(a)+'.jpg', t2], 'hide': 'hidden'}
