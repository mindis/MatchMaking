import os
import time
import random
import numpy as np
import tensorflow as tf
import tensorlayer as tl
from tensorlayer.layers import (Input, Conv2d,BatchNorm, BatchNorm2d, Elementwise, SubpixelConv2d, Flatten, Dense)
from tensorlayer.models import Model

   


def get_G(input_shape):
    w_init = tf.random_normal_initializer(stddev=0.02)
    g_init = tf.random_normal_initializer(1., 0.02)

    nin = Input(input_shape)
    n = Conv2d(64, (3, 3), (1, 1), act=tf.nn.relu, padding='SAME', W_init=w_init)(nin)
    temp = n

    # B residual blocks
    for i in range(16):
        nn = Conv2d(64, (3, 3), (1, 1), padding='SAME', W_init=w_init, b_init=None)(n)
        nn = BatchNorm2d(act=tf.nn.relu, gamma_init=g_init)(nn)
        nn = Conv2d(64, (3, 3), (1, 1), padding='SAME', W_init=w_init, b_init=None)(nn)
        nn = BatchNorm2d(gamma_init=g_init)(nn)
        nn = Elementwise(tf.add)([n, nn])
        n = nn

    n = Conv2d(64, (3, 3), (1, 1), padding='SAME', W_init=w_init, b_init=None)(n)
    n = BatchNorm(gamma_init=g_init)(n)
    n = Elementwise(tf.add)([n, temp])
    # B residual blacks end

    n = Conv2d(256, (3, 3), (1, 1), padding='SAME', W_init=w_init)(n)
    n = SubpixelConv2d(scale=2, n_out_channels=None, act=tf.nn.relu)(n)

    n = Conv2d(256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init)(n)
    n = SubpixelConv2d(scale=2, n_out_channels=None, act=tf.nn.relu)(n)

    nn = Conv2d(3, (1, 1), (1, 1), act=tf.nn.tanh, padding='SAME', W_init=w_init)(n)
    G = Model(inputs=nin, outputs=nn, name="generator")
    return G


#input_path ="gs://lr_images"
input_path ="input"
tl.files.exists_or_mkdir(input_path)
#file_name=*.jpeg

# Download all images from bucket "lr_images" to local directory
#!gsutil mv gs://nest-lr-images/*.png input/
os.system('gsutil mv gs://nest-lr-images/*.png input/')

#if __name__ == '__main__':
#save_dir = "gs://nest_hr_images"
output_path = "output"
tl.files.exists_or_mkdir(output_path)



#checkpoint_dir = "gs://nest-models"
models_path = "models"
tl.files.exists_or_mkdir(models_path)
os.system('gsutil cp gs://nest-models/g.h5 models/')

    
images_list = sorted(tl.files.load_file_list(path=input_path, regx='.*.png', printable=False))

print(images_list)
images = tl.vis.read_images(images_list, path=input_path, n_threads=2)



G = get_G([1, None, None, 3])
G.load_weights(os.path.join(models_path, 'g.h5'))
G.eval()



for i in range(0, len(images_list)):
    #print("Image name is ",images_list[i])
    #print("Image Shape is ",images[i].shape)
    if ( (images[i].shape[0] < 500 ) & (images[i].shape[1] < 500 ) ):
        valid_lr_img = images[i]
        valid_lr_img = (valid_lr_img / 127.5) - 1
        valid_lr_img = np.asarray(valid_lr_img, dtype=np.float32)
        valid_lr_img = valid_lr_img[np.newaxis,:,:,:]
        out = G(valid_lr_img).numpy()
        tl.vis.save_image(out[0], os.path.join(output_path, images_list[i]))
        rem_image= input_path+'/'+images_list[i]
        #print(rem_image)
        os.remove(rem_image)
    
    
#
    
os.system('gsutil mv output/*.png gs://nest-hr-images/')
os.system('gsutil mv input/*.png gs://nest-hr-images/')