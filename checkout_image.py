import os
import cv2
import shutil
images_path = "/Users/wangrui/Desktop/4343"

set_height = 32
set_width = 280

for file in os.listdir(images_path):
    for _ in file:
        if _ == " ":
            print(file)
            before_name = file
            after_name = file.replace(" ", "")
            shutil.move(os.path.join(images_path, before_name), os.path.join(images_path, after_name))
            file = after_name
            break

    image_path = os.path.join(images_path, file)
    n,_ = os.path.splitext(file)
    fff = n.split("_")
    if len(fff) != 2:
        print(file)
    img = cv2.imread(image_path)
    if img is None:
        print(image_path)
        continue


    h,w,_=img.shape
    after_width = set_height*w // h + 1
    if after_width > set_width:
        print(image_path)

