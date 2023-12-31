# -*- coding: utf-8 -*-
"""3D_Att_Res_U_Net.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eJG-gfR4f105xDUjla97wtsn0NZeBg-e
"""

from google.colab import drive
drive.mount('/content/gdrive')

# 1. Import Required Modules

import os
import glob
import keras
import random
import numpy as np
import tensorflow as tf
from keras.layers import *
import keras.backend as k
from keras.models import *
from keras.optimizers import *
import matplotlib.pyplot as plt
from skimage.transform import resize
from skimage.io import imread, imshow, imsave, imread_collection
from keras.losses import categorical_crossentropy
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping

# 2. Define Train & Test Path (Images + Mask Path for Train and Test Stages)

TRAIN_IMAGE_PATH = 'gdrive/My Drive/Berea_Sand_Texas/Image_Berea_UF_512_'
TRAIN_MASK_PATH = 'gdrive/My Drive/Berea_Sand_Texas/Mask_Berea_512_'

# 3. Initialize Images and Mask Size

IMG_HEIGHT, IMG_WIDTH, IMG_DEPTH, IMG_CHANNELS = 64, 64, 64, 1
input_shape = (IMG_HEIGHT, IMG_WIDTH, IMG_DEPTH, IMG_CHANNELS)

import glob
import cv2

Train_Input = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Parker_Sand/Image_512x512/*.png"))]
Train_Mask = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Parker_Sand/Label_512x512/*.png"))]

Train_Input = np.array(Train_Input)
Train_Mask = np.array(Train_Mask)

Train_Mask = cv2.normalize(Train_Mask, None, alpha=1,beta=0, norm_type=cv2.NORM_MINMAX)

import glob
import cv2

Train_Input_1 = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Berea_Sand/Image_Berea_UF_512/*.png"))]
Train_Mask_1 = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Berea_Sand/Mask_berea_512/*.png"))]

Train_Input_1 = np.array(Train_Input)
Train_Mask_1 = np.array(Train_Mask)

Train_Mask_1 = cv2.normalize(Train_Mask_1, None, alpha=1,beta=0, norm_type=cv2.NORM_MINMAX)

import glob
import cv2

Train_Input_2 = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Bandera_Gray_Sand/Image_512x512/*.png"))]
Train_Mask_2 = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Bandera_Gray_Sand/Label_512x512/*.png"))]

Train_Input_2 = np.array(Train_Input_2)
Train_Mask_2 = np.array(Train_Mask_2)

Train_Mask_2 = cv2.normalize(Train_Mask_2, None, alpha=1,beta=0, norm_type=cv2.NORM_MINMAX)

Train_Input_3D = np.stack(Train_Input, axis=2)
Train_Mask_3D = np.stack(Train_Mask, axis=2)

Train_Input_3D_1 = np.stack(Train_Input_1, axis=2)
Train_Mask_3D_1 = np.stack(Train_Mask_1, axis=2)

#Train_Input_3D_2 = np.stack(Train_Input_2, axis=2)
#Train_Mask_3D_2 = np.stack(Train_Mask_2, axis=2)

print(Train_Input_3D.shape)
print(Train_Input_3D_1.shape)
#print(Train_Input_3D_2.shape)

!pip install patchify

from patchify import *

Train_Input_3D_Patches = patchify(Train_Input_3D,(64,64,64), step=64)
Train_Mask_3D_Patches = patchify(Train_Mask_3D,(64,64,64), step=64)

Train_Input_3D_Patches_1 = patchify(Train_Input_3D_1,(64,64,64), step=64)
Train_Mask_3D_Patches_1 = patchify(Train_Mask_3D_1,(64,64,64), step=64)

#Train_Input_3D_Patches_2 = patchify(Train_Input_3D_2,(64,64,64), step=64)
#Train_Mask_3D_Patches_2 = patchify(Train_Mask_3D_2,(64,64,64), step=64)

print(Train_Mask_3D_Patches.shape)
print(Train_Mask_3D_Patches_1.shape)
#print(Train_Mask_3D_Patches_2.shape)

Train_Input_3D_Patche = np.reshape(Train_Input_3D_Patches, (-1, Train_Input_3D_Patches.shape[3], Train_Input_3D_Patches.shape[4], Train_Input_3D_Patches.shape[5]))
Train_Mask_3D_Patche = np.reshape(Train_Mask_3D_Patches, (-1, Train_Input_3D_Patches.shape[3], Train_Input_3D_Patches.shape[4], Train_Input_3D_Patches.shape[5]))

Train_Input_3D_Patche_1 = np.reshape(Train_Input_3D_Patches_1, (-1, Train_Input_3D_Patches_1.shape[3], Train_Input_3D_Patches_1.shape[4], Train_Input_3D_Patches_1.shape[5]))
Train_Mask_3D_Patche_1 = np.reshape(Train_Mask_3D_Patches_1, (-1, Train_Input_3D_Patches_1.shape[3], Train_Input_3D_Patches_1.shape[4], Train_Input_3D_Patches_1.shape[5]))

#Train_Input_3D_Patche_2 = np.reshape(Train_Input_3D_Patches_2, (-1, Train_Input_3D_Patches_2.shape[3], Train_Input_3D_Patches_2.shape[4], Train_Input_3D_Patches_2.shape[5]))
#Train_Mask_3D_Patche_2 = np.reshape(Train_Mask_3D_Patches_2, (-1, Train_Input_3D_Patches_2.shape[3], Train_Input_3D_Patches_2.shape[4], Train_Input_3D_Patches_2.shape[5]))

print(Train_Mask_3D_Patche.shape)
print(Train_Mask_3D_Patche_1.shape)
#print(Train_Mask_3D_Patche_2.shape)

Train_Input_3D_Patche = (Train_Input_3D_Patche, Train_Input_3D_Patche_1)  #, Train_Input_3D_Patche_2
Train_Mask_3D_Patche = (Train_Mask_3D_Patche, Train_Mask_3D_Patche_1)  #, Train_Mask_3D_Patche_2

Train_Input_3D_Patche = np.array(Train_Input_3D_Patche)
Train_Mask_3D_Patche = np.array(Train_Mask_3D_Patche)

Train_Input_3D_Patche = np.reshape(Train_Input_3D_Patche, (-1, Train_Input_3D_Patche.shape[2], Train_Input_3D_Patche.shape[3], Train_Input_3D_Patche.shape[4]))
Train_Mask_3D_Patche = np.reshape(Train_Mask_3D_Patche, (-1, Train_Mask_3D_Patche.shape[2], Train_Mask_3D_Patche.shape[3], Train_Mask_3D_Patche.shape[4]))

print(Train_Input_3D_Patche.shape)
print(Train_Mask_3D_Patche.shape)

def dice_loss(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.math.sigmoid(y_pred)
    numerator = 2 * tf.reduce_sum(y_true * y_pred)
    denominator = tf.reduce_sum(y_true + y_pred)

    return 1 - numerator / denominator

def jacard_coef(y_true, y_pred):
    y_true_f = k.flatten(y_true)
    y_pred_f = k.flatten(y_pred)
    intersection = k.sum(y_true_f * y_pred_f)
    return (intersection + 1.0) / (k.sum(y_true_f) + k.sum(y_pred_f) - intersection + 1.0)

def iou_coef(y_true, y_pred, smooth=1):
  intersection = k.sum(k.abs(y_true * y_pred), axis=[1,2])
  union = k.sum(y_true,[1,2])+k.sum(y_pred,[1,2])-intersection
  iou = k.mean((intersection+smooth) / (union+smooth), axis=0)
  return iou

def recall_m(y_true, y_pred):
    true_positives = k.sum(k.round(k.clip(y_true * y_pred, 0, 1)))
    possible_positives = k.sum(k.round(k.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + k.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = k.sum(k.round(k.clip(y_true * y_pred, 0, 1)))
    predicted_positives = k.sum(k.round(k.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + k.epsilon())
    return precision

def f1_m(y_true, y_pred):
   precision = precision_m(y_true, y_pred)
   recall = recall_m(y_true, y_pred)
   return 2*((precision*recall)/(precision+recall+k.epsilon()))

def Att_Res_U_Net_3D_Segmentation(input_size=(IMG_HEIGHT, IMG_WIDTH, IMG_DEPTH, IMG_CHANNELS)):

    inputs = Input(input_size)
    n = Lambda(lambda x:x/255)(inputs)


    c1 = Conv3D(16, (3,3,3), activation='relu', padding='same', kernel_initializer=tf.keras.initializers.Ones())(n)
    #c1 = BatchNormalization(axis=3)(c1)
    c1 = Dropout(0.1)(c1)
    c1 = Conv3D(16, (3,3,3), padding='same')(c1)
    #c1 = BatchNormalization(axis=3)(c1)
    shortcut1 = Conv3D(16, (1,1,1), padding='same')(n)
    #shortcut1 = BatchNormalization(axis=3)(shortcut1)

    Res_Path1 = add([shortcut1,c1])
    out1 = Activation('relu')(Res_Path1)

    p1 = MaxPooling3D((2,2,2))(out1)

    c2 = Conv3D(32, (3,3,3), activation='relu', padding='same')(p1)
    #c2 = BatchNormalization(axis=3)(c2)
    c2 = Dropout(0.1)(c2)
    c2 = Conv3D(32, (3,3,3), padding='same')(c2)
    #c2 = BatchNormalization(axis=3)(c2)
    shortcut2 = Conv3D(32, (1,1,1), padding='same')(p1)
    #shortcut2 = BatchNormalization(axis=3)(shortcut2)

    Res_Path2 = add([shortcut2,c2])
    out2 = Activation('relu')(Res_Path2)

    p2 = MaxPooling3D((2,2,2))(out2)


    c3 = Conv3D(64, (3,3,3), activation='relu', padding='same')(p2)
    #c3 =  BatchNormalization(axis=3)(c3)
    c3 = Dropout(0.2)(c3)
    c3 = Conv3D(64, (3,3,3), padding='same')(c3)
    #c3 =  BatchNormalization(axis=3)(c3)
    shortcut3 = Conv3D(64, (1,1,1), padding='same')(p2)
    #shortcut3 =  BatchNormalization(axis=3)(shortcut3)

    Res_Path3 = add([shortcut3,c3])
    out3 = Activation('relu')(Res_Path3)

    p3 = MaxPooling3D((2,2,2))(out3)


    c4 = Conv3D(128, (3,3,3), activation='relu', padding='same')(p3)
    #c4 =  BatchNormalization(axis=3)(c4)
    c4 = Dropout(0.2)(c4)
    c4 = Conv3D(128, (3,3,3), padding='same')(c4)
    #c4 =  BatchNormalization(axis=3)(c4)
    shortcut4 = Conv3D(128, (1,1,1), padding='same')(p3)
    #shortcut4 =  BatchNormalization(axis=3)(shortcut4)

    Res_Path4 = add([shortcut4,c4])
    out4 = Activation('relu')(Res_Path4)

    p4 = MaxPooling3D((2,2,2))(out4)


    c5 = Conv3D(256, (3,3,3), activation='elu', padding='same')(p4)
    #c5 =  BatchNormalization(axis=3)(c5)
    c5 = Dropout(0.3)(c5)
    c5 = Conv3D(256, (3,3,3), padding='same')(c5)
    #c5 = BatchNormalization(axis=3)(c5)
    shortcut5 = Conv3D(256, (1,1,1), padding='same')(p4)
    #shortcut5 =  BatchNormalization(axis=3)(shortcut5)

    Res_Path5 = add([shortcut5,c5])
    out5 = Activation('relu')(Res_Path5)


    u6 = Conv3DTranspose(128, (2,2,2), strides=(2,2,2), padding='same')(out5)


    theta_x_1 = Conv3D(64, (1,1,1), strides=(2,2,2), padding='same')(out4)
    #theta_x_1 = BatchNormalization(axis=3)(theta_x_1)
    shape_x_1 = k.int_shape(out4)
    phi_g_1 = Conv3D(64, (1,1,1), strides=(1,1,1), padding='same')(out5)
    #phi_g_1 = BatchNormalization(axis=3)(phi_g_1)
    conc_xg_1 = add([phi_g_1, theta_x_1])
    act_xg_1 = Activation('relu')(conc_xg_1)
    psi_1 = Conv3D(1, (1,1,1), strides=(1,1,1), padding='same')(act_xg_1)
    #psi_1 = BatchNormalization(axis=3)(psi_1)
    sigm_xg_1 = Activation('sigmoid')(psi_1)
    shape_sigm_1 = k.int_shape(sigm_xg_1)
    upsample_xg_1 = UpSampling3D(size=(shape_x_1[1]//shape_sigm_1[1], shape_x_1[2]//shape_sigm_1[2], shape_x_1[3]//shape_sigm_1[3]))(sigm_xg_1)
    y1 = multiply([upsample_xg_1, out4])


    conc6 = concatenate([u6, y1])

    c6 = Conv3D(128, (3,3,3), activation='relu', padding='same')(conc6)
    #c6 = BatchNormalization(axis=3)(c6)
    c6 = Dropout(0.2)(c6)
    c6 = Conv3D(128, (3,3,3), padding='same')(c6)
    #c6 = BatchNormalization(axis=3)(c6)
    shortcut6 = Conv3D(128, (1,1,1), padding='same')(u6)
    #shortcut6 = BatchNormalization(axis=3)(shortcut6)

    Res_Path6 = add([shortcut6,c6])
    out6 = Activation('relu')(Res_Path6)


    u7 = Conv3DTranspose(64, (2,2,2), strides=(2,2,2), padding='same')(out6)


    theta_x_2 = Conv3D(128, (1,1,1), strides=(2,2,2), padding='same')(out3)
    #theta_x_2 = BatchNormalization(axis=3)(theta_x_2)
    shape_x_2 = k.int_shape(out3)
    phi_g_2 = Conv3D(128, (1,1,1), strides=(1,1,1), padding='same')(out6)
    #phi_g_2 = BatchNormalization(axis=3)(phi_g_2)
    conc_xg_2 = add([phi_g_2, theta_x_2])
    act_xg_2 = Activation('relu')(conc_xg_2)
    psi_2 = Conv3D(1, (1,1,1), strides=(1,1,1), padding='same')(act_xg_2)
    #psi_2 = BatchNormalization(axis=3)(psi_2)
    sigm_xg_2 = Activation('sigmoid')(psi_2)
    shape_sigm_2 = k.int_shape(sigm_xg_2)
    upsample_xg_2 = UpSampling3D(size=(shape_x_2[1]//shape_sigm_2[1], shape_x_2[2]//shape_sigm_2[2], shape_x_2[3]//shape_sigm_2[3]))(sigm_xg_2)
    y2 = multiply([upsample_xg_2, out3])


    conc7 = concatenate([u7, y2])

    c7 = Conv3D(64, (3,3,3), activation='relu', padding='same')(conc7)
    #c7 = BatchNormalization(axis=3)(c7)
    c7 = Dropout(0.2)(c7)
    c7 = Conv3D(64, (3,3,3), padding='same')(c7)
    #c7 = BatchNormalization(axis=3)(c7)
    shortcut7 = Conv3D(64, (1,1,1), padding='same')(u7)
    #shortcut7 = BatchNormalization(axis=3)(shortcut7)

    Res_Path7 = add([shortcut7,c7])
    out7 = Activation('relu')(Res_Path7)


    u8 = Conv3DTranspose(32, (2,2,2), strides=(2,2,2), padding='same')(out7)


    theta_x_3 = Conv3D(256, (1,1,1), strides=(2,2,2), padding='same')(out2)
    #theta_x_3 = BatchNormalization(axis=3)(theta_x_3)
    shape_x_3 = k.int_shape(out2)
    phi_g_3 = Conv3D(256, (1,1,1), strides=(1,1,1), padding='same')(out7)
    #phi_g_3 = BatchNormalization(axis=3)(phi_g_3)
    conc_xg_3 = add([phi_g_3, theta_x_3])
    act_xg_3 = Activation('relu')(conc_xg_3)
    psi_3 = Conv3D(1, (1,1,1), strides=(1,1,1), padding='same')(act_xg_3)
    #psi_3 = BatchNormalization(axis=3)(psi_3)
    sigm_xg_3 = Activation('sigmoid')(psi_3)
    shape_sigm_3 = k.int_shape(sigm_xg_3)
    upsample_xg_3 = UpSampling3D(size=(shape_x_3[1]//shape_sigm_3[1], shape_x_3[2]//shape_sigm_3[2], shape_x_3[3]//shape_sigm_3[3]))(sigm_xg_3)
    y3 = multiply([upsample_xg_3, out2])


    conc8 = concatenate([u8, y3])

    c8 = Conv3D(32, (3,3,3), activation='relu', padding='same')(conc8)
    #c8 = BatchNormalization(axis=3)(c8)
    c8 = Dropout(0.1)(c8)
    c8 = Conv3D(32, (3,3,3), padding='same')(c8)
    #c8 = BatchNormalization(axis=3)(c8)
    shortcut8 = Conv3D(32, (1,1,1), padding='same')(u8)
    #shortcut8 = BatchNormalization(axis=3)(shortcut8)

    Res_Path8 = add([shortcut8,c8])
    out8 = Activation('relu')(Res_Path8)


    u9 = Conv3DTranspose(16, (2,2,2), strides=(2,2,2), padding='same')(out8)


    theta_x_4 = Conv3D(512, (1,1,1), strides=(2,2,2), padding='same')(out1)
    #theta_x_4 = BatchNormalization(axis=3)(theta_x_4)
    shape_x_4 = k.int_shape(out1)
    phi_g_4 = Conv3D(512, (1,1,1), strides=(1,1,1), padding='same')(out8)
    #phi_g_4 = BatchNormalization(axis=3)(phi_g_4)
    conc_xg_4 = add([phi_g_4, theta_x_4])
    act_xg_4 = Activation('relu')(conc_xg_4)
    psi_4 = Conv3D(1, (1,1,1), strides=(1,1,1), padding='same')(act_xg_4)
    #psi_4 = BatchNormalization(axis=3)(psi_4)
    sigm_xg_4 = Activation('sigmoid')(psi_4)
    shape_sigm_4 = k.int_shape(sigm_xg_4)
    upsample_xg_4 = UpSampling3D(size=(shape_x_4[1]//shape_sigm_4[1], shape_x_4[2]//shape_sigm_4[2], shape_x_4[3]//shape_sigm_4[3]))(sigm_xg_4)
    y4 = multiply([upsample_xg_4, out1])


    conc9 = concatenate([u9, y4], axis = 4)

    c9 = Conv3D(16, (3,3,3), activation='relu', padding='same')(conc9)
    #c9 = BatchNormalization(axis=3)(c9)
    c9 = Dropout(0.1)(c9)
    c9 = Conv3D(16, (3,3,3), padding='same')(c9)
    #c9 = BatchNormalization(axis=3)(c9)
    shortcut9 = Conv3D(16, (1,1,1), padding='same')(u9)
    #shortcut9 = BatchNormalization(axis=3)(shortcut9)

    Res_Path9 = add([shortcut9,c9])
    out9 = Activation('relu')(Res_Path9)


    outputs = Conv3D(1,(1,1,1), activation='sigmoid')(out9)

    model = Model(inputs=[inputs], outputs=[outputs])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005), loss = ['binary_crossentropy'], metrics=[tf.keras.metrics.IoU(num_classes=2, target_class_ids=[0, 1]), tf.keras.metrics.IoU(num_classes=2, target_class_ids=[0]), tf.keras.metrics.IoU(num_classes=2, target_class_ids=[1]), f1_m ,precision_m , recall_m, 'accuracy', jacard_coef])
    model.summary()
    return model

model = Att_Res_U_Net_3D_Segmentation()

Model_Path = 'gdrive/My Drive/Saved_Models/3D_Att_Res_U_Net/Parker_Berea_IOU_F1_JC_ACC_3D_Att_Res_U_Net_Ones_0005'

earlystopper = EarlyStopping(patience=20, verbose=1)
checkpointer = ModelCheckpoint(Model_Path, verbose = 1, save_best_only=True)

Validation_Input_3D_Patche = Train_Input_3D_Patche[:384]
Train_Input_3D_Patche = Train_Input_3D_Patche[384:]
Validation_Mask_3D_Patche = Train_Mask_3D_Patche[:384]
Train_Mask_3D_Patche = Train_Mask_3D_Patche[384:]

print(Validation_Input_3D_Patche.shape)
print(Validation_Mask_3D_Patche.shape)
print(Train_Input_3D_Patche.shape)
print(Train_Mask_3D_Patche.shape)

# 8. Train U_NET Model using Training Samples

results = model.fit(Train_Input_3D_Patche, Train_Mask_3D_Patche,
                    validation_data=(Validation_Input_3D_Patche, Validation_Mask_3D_Patche),
                    batch_size=2,
                    epochs=100,
                    callbacks=[checkpointer])
#callbacks=[earlystopper, checkpointer, loss_history()]

# 11. Show Loss and ACC Plots


# 11.1. Summarize History for Loss

plt.plot(results.history['loss'])
plt.plot(results.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epochs')
plt.legend(['Training','Validation'], loc = 'upper left')
plt.show()


# 11.1. Summarize History for IOU

plt.plot(results.history['io_u_3'])
plt.plot(results.history['val_io_u_3'])
plt.title('Yotal IOU')
plt.ylabel('T-IOU')
plt.xlabel('epochs')
plt.legend(['Training','Validation'], loc = 'upper left')
plt.show()


# 11.1. Summarize History for IOU

plt.plot(results.history['io_u_4'])
plt.plot(results.history['val_io_u_4'])
plt.title('Pore IOU')
plt.ylabel('P-IOU')
plt.xlabel('epochs')
plt.legend(['Training','Validation'], loc = 'upper left')
plt.show()

# 11.1. Summarize History for IOU

plt.plot(results.history['io_u_5'])
plt.plot(results.history['val_io_u_5'])
plt.title('Matrix IOU')
plt.ylabel('M-IOU')
plt.xlabel('epochs')
plt.legend(['Training','Validation'], loc = 'upper left')
plt.show()


# 11.1. Summarize History for Jacard Coef

plt.plot(results.history['jacard_coef'])
plt.plot(results.history['val_jacard_coef'])
plt.title('Jaccard Coefficient')
plt.ylabel('JC')
plt.xlabel('epochs')
plt.legend(['Training','Validation'], loc = 'upper left')
plt.show()

Test_Input = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Image_512x512/*.png"))]
Test_Mask = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Label_512x512/*.png"))]

Test_Input = np.array(Test_Input)
Test_Mask = np.array(Test_Mask)

Test_Mask = cv2.normalize(Test_Mask, None, alpha=1,beta=0, norm_type=cv2.NORM_MINMAX)

Test_Input_3D = np.stack(Test_Input, axis=2)
Test_Mask_3D = np.stack(Test_Mask, axis=2)

Test_Input_3D_Patches = patchify(Test_Input_3D,(128,128,128), step=128)
Test_Mask_3D_Patches = patchify(Test_Mask_3D,(128,128,128), step=128)

Test_Input_3D_Patche = np.reshape(Test_Input_3D_Patches, (-1, Test_Input_3D_Patches.shape[3], Test_Input_3D_Patches.shape[4], Test_Input_3D_Patches.shape[5]))
Test_Mask_3D_Patche = np.reshape(Test_Mask_3D_Patches, (-1, Test_Input_3D_Patches.shape[3], Test_Input_3D_Patches.shape[4], Test_Input_3D_Patches.shape[5]))

Test_Mask_3D_Patche.shape

Results = model.evaluate(Test_Input_3D_Patche, Test_Mask_3D_Patche, batch_size=2)

Test_Input_1 = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Buff_Berea_Sand/Image_512x512/*.png"))]
Test_Mask_1 = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Buff_Berea_Sand/Label_512x512/*.png"))]

Test_Input_1 = np.array(Test_Input_1)
Test_Mask_1 = np.array(Test_Mask_1)

Test_Mask_1 = cv2.normalize(Test_Mask_1, None, alpha=1,beta=0, norm_type=cv2.NORM_MINMAX)

Test_Input_3D_1 = np.stack(Test_Input_1, axis=2)
Test_Mask_3D_1 = np.stack(Test_Mask_1, axis=2)

Test_Input_3D_Patches_1 = patchify(Test_Input_3D_1,(128,128,128), step=128)
Test_Mask_3D_Patches_1 = patchify(Test_Mask_3D_1,(128,128,128), step=128)

Test_Input_3D_Patche_1 = np.reshape(Test_Input_3D_Patches_1, (-1, Test_Input_3D_Patches_1.shape[3], Test_Input_3D_Patches_1.shape[4], Test_Input_3D_Patches_1.shape[5]))
Test_Mask_3D_Patche_1 = np.reshape(Test_Mask_3D_Patches_1, (-1, Test_Input_3D_Patches_1.shape[3], Test_Input_3D_Patches_1.shape[4], Test_Input_3D_Patches_1.shape[5]))

Test_Mask_3D_Patche_1.shape

Results = model.evaluate(Test_Input_3D_Patche_1, Test_Mask_3D_Patche_1, batch_size=2)

Test_Input_2 = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Berea_Sand_Texas/Image_Berea_UF_512_/*.png"))]
Test_Mask_2 = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in sorted(glob.glob("gdrive/My Drive/Berea_Sand_Texas/Mask_Berea_512_/*.png"))]

Test_Input_2 = np.array(Test_Input_2)
Test_Mask_2 = np.array(Test_Mask_2)

Test_Mask_2 = cv2.normalize(Test_Mask_2, None, alpha=1,beta=0, norm_type=cv2.NORM_MINMAX)

Test_Input_3D_2 = np.stack(Test_Input_2, axis=2)
Test_Mask_3D_2 = np.stack(Test_Mask_2, axis=2)

Test_Input_3D_Patches_2 = patchify(Test_Input_3D_2,(128,128,128), step=128)
Test_Mask_3D_Patches_2 = patchify(Test_Mask_3D_2,(128,128,128), step=128)

Test_Input_3D_Patche_2 = np.reshape(Test_Input_3D_Patches_2, (-1, Test_Input_3D_Patches_2.shape[3], Test_Input_3D_Patches_2.shape[4], Test_Input_3D_Patches_2.shape[5]))
Test_Mask_3D_Patche_2 = np.reshape(Test_Mask_3D_Patches_2, (-1, Test_Input_3D_Patches_2.shape[3], Test_Input_3D_Patches_2.shape[4], Test_Input_3D_Patches_2.shape[5]))

Test_Mask_3D_Patche_2.shape

Results = model.evaluate(Test_Input_3D_Patche_2, Test_Mask_3D_Patche_2, batch_size=2)