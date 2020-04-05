import os
import cv2
images_path = "/Users/wangrui/Desktop/899"

set_height = 32
set_width = 280

for file in os.listdir(images_path):
    image_path = os.path.join(images_path, file)
    n,_ = os.path.splitext(file)
    fff = n.split("_")
    if len(fff) != 2:
        print(file)
    img = cv2.imread(image_path)
    h,w,_=img.shape
    after_width = set_height*w // h + 1
    if after_width > set_width:
        print(image_path)

