import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import cv2
import keras

# Load the dataset
data_path = "fabric.jpg"
defect_types = os.listdir(data_path)
num_classes = len(defect_types)

X = []
y = []
for i, defect_type in enumerate(defect_types):
    class_path = os.path.join(data_path, defect_type)
    for img_path in os.listdir(class_path):
        img = cv2.imread(os.path.join(class_path, img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to RGB format
        img = cv2.resize(img, (224, 224))  # resize to match VGG16 input size
        X.append(img)
        y.append(i)

X = np.array(X)
y = np.array

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load the pre-trained VGG16 model
from tensorflow.keras.applications.vgg16 import VGG16

base_model = VGG16(input_shape=(224, 224, 3), include_top=False, weights='imagenet')

# Freeze the layers in the base model
for layer in base_model.layers:
    layer.trainable = False

# Add a custom classification head
x = tf.keras.layers.Flatten()(base_model.output)
x = tf.keras.layers.Dense(256, activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
x = tf.keras.layers.Dense(num_classes, activation='softmax')(x)

# Create the model
model = tf.keras.models.Model(inputs=base_model.input, outputs=x)

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test))

# Evaluate the model on the test set
model.evaluate(X_test, y_test)

# Save the model
model.save("fabric_defect_model.h5")