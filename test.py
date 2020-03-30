import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, default='', help="path of images or dir")
parser.add_argument('--model', type=str, default='models/keras_model', help="keras model(include weights and model) path")
parser.add_argument('--label', type=str, default='models/label_map.txt', help="label to text")
parser.add_argument('--show', type=bool, default=True, help="show image when after test by UI")
args = parser.parse_args()
import os
import tensorflow as tf
import cv2
import numpy
import tensorflow.keras.backend as K
model = tf.keras.models.load_model(args.model)
with open(args.label_map, "r") as f:
    alphabet = f.read()
nclass = len(alphabet) + 1
# Reverse translation of numerical classes back to characters
def labels_to_text(labels):
    ret = []
    print(labels)
    for c in labels:
        print(c)
        if c == len(alphabet):  # CTC Blank
            ret.append("")
        else:
            ret.append(alphabet[c])
    return "".join(ret)
def decode(pred):
    char_list = []
    pred_text = pred.argmax(axis=1)
    print("shape: ", pred_text.shape)
    print(pred_text)
    for i in range(len(pred_text)):
        if pred_text[i] != nclass - 1 and ((not (i > 0 and pred_text[i] == pred_text[i - 1])) or (i > 1 and pred_text[i] == pred_text[i - 2])):
            char_list.append(alphabet[pred_text[i]])
    return u''.join(char_list)
def predict(img):
    height, width, _ = img.shape
    scale = height * 1.0 / 32
    width = int(width / scale)
    img = cv2.resize(img, (width, 32))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    from src.utils import wrapper_image
    input_data = numpy.ones((1, 32, width, 1), dtype=numpy.float)
    img = wrapper_image(img)
    input_data[0,:,:,0] = img

    '''
    img_array = np.array(img.convert('1'))
    boundary_array = np.concatenate((img_array[0, :], img_array[:, width - 1], img_array[31, :], img_array[:, 0]), axis=0)
    if np.median(boundary_array) == 0:  # 将黑底白字转换为白底黑字
        img = ImageOps.invert(img)
    '''
    out = model.predict([input_data])[0]
    #out = K.get_value(K.ctc_decode(y_pred, input_length=numpy.ones(y_pred.shape[0]) * y_pred.shape[1])[0][0])[:, :]
    res = decode(out)
    return res

def test_dir(dir_path, ishow=True):
    files = os.listdir(dir_path)
    for file in files:
        img = cv2.imread(os.path.join(dir_path, file))
        res = predict(img)
        print("file {} result: {}".format(file, res))
        if ishow:
            cv2.imshow("demo", img)
            cv2.waitKey(0)

def test_file(file_path, ishow=True):
    img = cv2.imread(file_path)
    res = predict(img)
    print("file {} result: {}".format(file_path, res))
    if ishow:
        cv2.imshow("demo", img)
        cv2.waitKey(0)

if __name__ == '__main__':
    assert os.path.exists(args.file)

    if os.path.isdir(args.file):
        test_dir(args.file, args.show)
    else:
        test_file(args.file, args.show)
