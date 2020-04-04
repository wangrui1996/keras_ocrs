import os
import shutil
dataset_path = os.path.join(os.environ["HOME"], "Dataset", "ocrs")

dataset_label_txt_path = os.path.join(dataset_path, "data_train.txt")
new_label_txt_path = os.path.join(dataset_path, "custom_data_train.txt")
custom_images_path = os.path.join(dataset_path, "custom_images")
if not os.path.exists(custom_images_path):
    os.mkdir(custom_images_path)

shutil.copy(dataset_label_txt_path, new_label_txt_path)

custom_image_files = os.listdir(custom_images_path)

custom_number = len(custom_image_files)

def add(image_files):
    for file in image_files:
        label = os.path.splitext(file)[0].split("_")[1]
        with open(new_label_txt_path, "a") as output_file:
            output_file.writelines("{} {}\n".format(file, label))
    #label = str(file).split(".")[0].split("_")[1]
    #if len(label) >1:
    #    print(label)

times = 3600000//(custom_number * 100)

for i in range(times):
    add(custom_image_files)




