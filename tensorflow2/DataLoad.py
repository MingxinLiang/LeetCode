#! /usr/bin/python
from email.mime import image
from importlib.resources import path
from numpy import imag
import tensorflow as tf

Autotune = tf.data.experimental.AUTOTUNE

import pathlib
data_root_orig = tf.keras.utils.get_file(origin='https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
                                         fname='flower_photos', untar=True)
data_root = pathlib.Path(data_root_orig)
print(data_root)

for item in data_root.iterdir():
    print(item)

import random
all_image_paths = list(data_root.glob('*/*'))
all_image_paths = [str(path) for path in all_image_paths]
random.shuffle(all_image_paths)

image_count = len(all_image_paths)
print("Total image:", image_count)

import os
attributions = (data_root/"LICENSE.txt").open(encoding="utf-8").readlines()[4:]
attributions = [line.split(' CC-BY') for line in attributions]
attributions = dict(attributions)

#import IPython.display as display
#
#def caption_image(image_path):
#    image_rel = pathlib.Path(image_path).relative_to(data_root)
#    return "Image (CC BY 2.0) " + ' - '.join(attributions[str(image_rel)].split(' - ')[:-1])
#
#
#for n in range(3):
#    image_path = random.choice(all_image_paths)
#    display.display(display.Image(image_path))
#    print(caption_image(image_path))
#    print()

label_names = sorted(item.name for item in data_root.glob("*/") if item.is_dir())

label_to_idx = dict((name, index) for index, name in enumerate(label_names))

all_image_labels = [label_to_idx[pathlib.Path(path).parent.name]
                    for path in all_image_paths]

#img_path = all_image_paths[0]
#img_raw = tf.io.read_file(img_path)
#img_tensor = tf.image.decode_image(img_raw)
#
#print(img_tensor)

def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [192, 192])
    image /= 255.0

    return image

def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)

# prepare image and label
path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)
image_ds = path_ds.map(load_and_preprocess_image, num_parallel_calls=Autotune)
label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))

image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))

# trainning
BATCH_SIZE = 32
ds = image_label_ds.shuffle(buffer_size=image_count)
ds = ds.repeat()
ds = ds.batch(BATCH_SIZE)
ds = ds.prefetch(buffer_size=Autotune)

# get mobile net feature
mobile_net = tf.keras.applications.MobileNetV2(input_shape=(192, 192, 3), include_top = False)
mobile_net.trainable = False

def change_range(image, label):
    return 2*image - 1, label

keras_ds = ds.map(change_range)

image_batch, label_batch = next(iter(keras_ds))

feature_map_batch = mobile_net(image_batch)

# buil model
model = tf.keras.Sequential([
    mobile_net,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(len(label_names), activation="softmax")
])

#logit_batch = model(image_batch).numpy()
#
#print("min logit:", logit_batch.min())
#print("max logit:", logit_batch.max())
#print("Shape:", logit_batch.shape)

# train model
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss = "sparse_categorical_crossentropy",
              metrics = ["accuracy"])

model.summary()

#steps_per_epoch = 3
steps_per_epoch = 115
#model.fit(ds, epochs = 1, steps_per_epoch=3)

import time
default_timeit_steps = 2 * steps_per_epoch + 1

# 缓存优化
def timeit(ds, steps = default_timeit_steps):
    overall_start = time.time()
    it = iter(ds.take(steps+1))
    next(it)

    start = time.time()
    for i, (images, labels) in enumerate(it):
        if i % 10 == 0:
            print('.', end = '')
    print()
    end = time.time()

    duration = end - start

    print("{} batches: {}s".format(steps, duration))
    print("{:0.5f} Images/s".format(BATCH_SIZE*steps/duration))
    print("Total Time: {}s".format(end - overall_start))

ds = image_label_ds.cache(filename='./cache.tf-data')
ds = image_label_ds.apply(
    tf.data.experimental.shuffle_and_repeat(buffer_size=image_count)
)

ds = ds.batch(BATCH_SIZE).prefetch(buffer_size=0)

#timeit(ds)

# TFRecord