import os
import numpy as np

import argparse
parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--gpus', default="", help='number of gpu to train')
args = parser.parse_args()

if args.gpus is not "":
    os.environ["CUDA_VISIBLE_DEVICES"] = "{}".format(args.gpus)

from tensorflow.python import keras
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.layers import Input
from tensorflow.python.keras.layers.core import Reshape, Masking, Lambda, Permute
from tensorflow.python.keras.models import Model
from src.models import densenet
from src.utils import DataGenerator

np.random.seed(55)

class VizCallback(keras.callbacks.Callback):

    def __init__(self, base_model, model_save_path):
        self.output_dir = model_save_path
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.base_model = base_model

    def on_epoch_end(self, epoch, logs={}):
        #self.model.save_weights(
        #    os.path.join(self.output_dir, 'weights%02d.h5' % (epoch)))
        self.base_model.save(os.path.join(self.output_dir, 'model%02d' % (epoch)))
        #out_path = os.path.join(self.output_dir,"ocrs.tflite")
        # Convert the model.
        #converter = tf.lite.TFLiteConverter.from_keras_model(model)
        #tflite_model = converter.convert()
        #with open(out_path, "wb") as f:
        #    f.write(tflite_model)

def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args
    # the 2 is critical here since the first couple outputs of the RNN
    # tend to be garbage:
    #y_pred = y_pred[:, 2:-2, :]
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)

def get_model(img_h, nclass):
    input = Input(shape=(img_h, None, 1), name='the_input')
    y_pred = densenet.dense_cnn(input, nclass)

    basemodel = Model(inputs=input, outputs=y_pred)
    basemodel.summary()

    labels = Input(name='the_labels', shape=[None], dtype='float32')
    input_length = Input(name='input_length', shape=[1], dtype='int64')
    label_length = Input(name='label_length', shape=[1], dtype='int64')

    loss_out = Lambda(
        ctc_lambda_func, output_shape=(1,),
        name='ctc')([y_pred, labels, input_length, label_length])
    model = Model(inputs=[input, labels, input_length, label_length], outputs=loss_out)
    # clipnorm seems to speeds up convergence
    #sgd = SGD(learning_rate=0.02,
    #          decay=1e-6,
    #          momentum=0.9,
    #          nesterov=True)
    #model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=sgd)
    model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer='adam', metrics=['accuracy'])

    return basemodel, model




if __name__ == '__main__':
    img_w = 280
    img_h = 32
    batch_size = 128
    model_save_path = "./save_models"
    train_img_gen = DataGenerator(
        batch_size=batch_size,
        img_w=img_w,
        img_h=img_h,
        downsample_factor=4,
        label_map = os.path.join(os.getcwd(), os.path.join(model_save_path, "label_map.txt"))
    )
    test_img_gen = DataGenerator(
        batch_size=batch_size,
        img_w=img_w,
        img_h=img_h,
        downsample_factor=4)

    user_root_path = os.environ['HOME']
    ocrs_dataset_path = os.path.join(user_root_path, "Dataset", "ocrs")
    train_img_gen.set_dataset(os.path.join(ocrs_dataset_path, "images"), os.path.join(ocrs_dataset_path, "custom_data_train.txt"), train=True)
    test_img_gen.set_dataset(os.path.join(ocrs_dataset_path, "images"), os.path.join(ocrs_dataset_path, "data_test.txt"), train=False)

    base_model, model = get_model(img_h, train_img_gen.get_output_size())

    modelPath = './models/keras_model'
    if os.path.exists(modelPath):
        print("Loading model weights...")
        base_model.load_weights(modelPath, by_name=True)
        print('done!')
    #test_func = K.function([basemodel.input], [basemodel.output])
    #viz_cb = VizCallback(test_func, model_save_path=model_save_path)
    viz_cb = VizCallback(base_model, model_save_path=model_save_path)
    print('-----------Start training-----------')
    model.fit_generator(
        generator=train_img_gen,
        steps_per_epoch=5,
        epochs=10,
        validation_data=test_img_gen,
        validation_steps=5,
        callbacks=[viz_cb],
        workers=12,
        use_multiprocessing=True,

    )
    #model.fit_generator(
    #    train_img_gen.next_train(),
    #    steps_per_epoch = 3607567 // batch_size,
    #	epochs = 100,
    #	initial_epoch = 0,
    #	validation_data = test_img_gen.next_val(),
    #	validation_steps = 36440 // batch_size,
    #	callbacks = [viz_cb, train_img_gen],
    #   workers=1,
    #   use_multiprocessing = True)

