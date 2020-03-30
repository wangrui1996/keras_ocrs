import os
import cv2
import numpy
import random
src_image_path = "/Users/wangrui/Desktop/data"
dst_image_path = "/Users/wangrui/Desktop/new_images"
label_path = ""

image_files = os.listdir(src_image_path)

top_num = 1000


def crop_image(image, threshold=2):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = (255 - cv2.Canny(gray, 200, 200)) / 255
    # print(binary)
    # ret, binary = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("demo", binary)
    # cv2.waitKey(0)
    binary = numpy.ones(binary.shape) - binary
    binary_map = numpy.sum(binary, axis=1)
    start = 0
    stay_upper = False
    list_images = []
    for idx in range(len(binary_map)):
        if binary_map[idx] > threshold:
            if stay_upper:
                continue
            else:
                stay_upper = True
                start = idx
        else:
            if stay_upper:
                end = idx
                stay_upper = False
                if end - start < 10:
                    continue
                else:
                    start = max(0, random.randint(start - 5, start))
                    end = min(random.randint(end, end+5), len(binary_map))
                    crop_img = image[start:end, :, :]
                    list_images.append(crop_img)
            else:
                continue
    if len(list_images) == 0:
        return image

    if len(list_images) == 1:
        return list_images[0]

    def rescale_img(img, scale_height=32):
        height, width,_ = img.shape
        scale = height * 1.0 / scale_height
        width = int(width / scale)
        img = cv2.resize(img, (width, 32))
        return img

    re_img = rescale_img(list_images[0])
    for image_ in list_images[1:]:
        re_img = numpy.hstack((re_img, rescale_img(image_)))
    return re_img

def crop_image_width(image, threshold=1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = (255 - cv2.Canny(gray, 200, 200)) / 255
    # print(binary)
    # ret, binary = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow("binary", binary*255)
    # cv2.waitKey(0)
    binary = numpy.ones(binary.shape) - binary
    binary_map = numpy.sum(binary, axis=0)
    start = 0
    stay_upper = False
    width_start=0
    width_end = len(binary_map) - 1
    print("result: ")
    print(len(binary_map))
    for idx in range(len(binary_map)):
        if binary_map[idx] > threshold:
            if stay_upper:
                continue
            else:
                stay_upper = True
                start = idx
        else:
            if stay_upper:
                end = idx
                stay_upper = False
                if end - start < 2:
                    continue
                else:
                    width_start = max(0, random.randint(start - 10, start))
                    break
                    #end = min(end + 5, len(binary_map))
                    #crop_img = image[start:end, :, :]
                    #list_images.append(crop_img)
            else:
                continue
    print("start: ", width_start)
    stay_upper = False
    for idx in range(len(binary_map)-1, -1, -1):
        if binary_map[idx] > threshold:
            if stay_upper:
                continue
            else:
                stay_upper = True
                end = idx
        else:
            if stay_upper:
                start = idx
                stay_upper = False
                if end - start < 2:
                    continue
                else:
                    width_end = min(random.randint(end+5, end + 10), len(binary_map)-1)
                    break
                    #end = min(end + 5, len(binary_map))
                    #crop_img = image[start:end, :, :]
                    #list_images.append(crop_img)
            else:
                continue
    print(width_start, width_end)
    if width_end <= width_start:
        return image

    return image[:,width_start:width_end,:]
import shutil
dataset_label_txt_path = "/Users/wangrui/Downloads/DataSet/tmp.txt"
new_label_txt_path = "/Users/wangrui/Downloads/DataSet/tmp_a.txt"

shutil.copy(dataset_label_txt_path, new_label_txt_path)


img_idx = 0
for _ in range(top_num):
    file_name = random.choice(image_files)
    image_path = os.path.join(src_image_path, file_name)
    label = str(file_name).split(".")[0].split("_")[1]
    #output_file.write("{} {}".format(file_name, label))
    img = cv2.imread(image_path)
    cv2.imshow("source", img)
    img = crop_image(img)
    cv2.imshow("tmp", img)
    img = crop_image_width(img)
    new_file_name = "custom{}_{}.{}".format(img_idx, str(file_name).split(".")[0].split("_")[-1], str(file_name).split(".")[-1])
    img_idx = img_idx+1
    print("new file name: ", new_file_name, label)
    cv2.imwrite(os.path.join(dst_image_path, new_file_name), img)

    with open(new_label_txt_path, "a") as output_file:
        output_file.writelines("{} {}\n".format(new_file_name, label))
    cv2.imshow("fina", img)
    cv2.waitKey(0)
    #file_name = file_name.replace(".jpg", "")
    #print(file_name)
    #print(str(file_name).split("_")[1])