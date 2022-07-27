import pytesseract
import requests
import numpy as np
import cv2
import urllib

img_url = 'http://yiyt.tcm.tw/showpic.php'
req = urllib.request.urlopen(img_url)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1) # 'Load it as it is'

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# config = '--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789' # not bad 1
# config = '--psm 12 --oem 3 -c tessedit_char_whitelist=0123456789' # not bad 2
# config = '--psm 4 --oem 3 -c tessedit_char_whitelist=0123456789' # not bad 3
config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789' # not bad 3
orc = pytesseract.image_to_string(img, config=config)
print(orc) # 印出辨識的文字

cv2.imshow('lalala', img)
cv2.waitKey(0)



# print(img_url)
# resp = requests.get(img_url)
# print(resp)
# image = np.asarray(bytearray(resp.read()), dtype="uint8")
# image = cv2.imdecode(image, cv2.IMREAD_COLOR)
# cv2.imshow(image)
# cv2.waitKey(0)