import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
import tkinter as tk
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def detect_defects_in_folder(folder_path):
    # Load the saved model
    model = tf.keras.models.load_model('fabric_defect_model.h5')

    # Initialize variables to keep track of defected images and their types
    defected_images = {'Hole': 0, 'Lines': 0, 'Stain': 0,'Good':0}
    labels = []

    # Iterate over each image in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.jfif'):
            # Load the image
            image_path = os.path.join(folder_path, filename)
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Preprocess the image
            new_image = cv2.resize(img, (224, 224))
            new_image = np.expand_dims(new_image, axis=0)

            # Classify the image
            predictions = model.predict(new_image)
            predicted_class = np.argmax(predictions)

            # Get the class label
            classes = ['Good', 'Hole', 'Lines', 'Stain']
            predicted_label = classes[predicted_class]

            if predicted_label != 'Good':
                # Increment the count of defected images of this type
                defected_images[predicted_label] += 1

                # Convert the image to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Apply thresholding to segment the fabric
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Apply thresholding to segment the fabric
                thresh_value = 155
                ret, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY_INV)
                # Find the contours of the fabric
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Initialize an empty list to store defects
                defects = []

                # Iterate through each contour and calculate the total area and defected area
                total_area = img.shape[0] * img.shape[1]
                defected_area = 0
                for cnt in contours:
                    # Get the bounding rectangle of the contour
                    x, y, w, h = cv2.boundingRect(cnt)

                    # Calculate the area of the contour
                    area = cv2.contourArea(cnt)

                    # Calculate the percentage of defected area for the contour
                    percentage_area = area / total_area * 100

                    # Check if the percentage of defected area is greater than a threshold value
                    if percentage_area > 0.5:
                        # Add the defect to the list
                        defects.append((x, y, w, h))
                        defected_area += w * h

                # Calculate the percentage of the defected area
                percentage_defected_area = defected_area / total_area * 100

                # Plot the image with the defects marked
                fig, ax = plt.subplots()
                ax.imshow(img)

                for defect in defects:
                    x, y, w, h = defect
                    rect = plt.Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=2)
                    ax.add_patch(rect)

                ax.set_title(f'Predicted Label: {predicted_label}')
                plt.axis('off')
                plt.show()


                # Add the label to the list of labels
                labels.append(predicted_label)

            else:
                defected_images['Good'] += 1
                labels.append('Good')

    # Print the summary
    total_images = len(labels)
    print(f'Total Images: {total_images}')
    print(f'Total Defected Images: {total_images - defected_images["Good"]}')
    for label, count in defected_images.items():
            print(f'{label} Images: {count}, Percentage: {count/(total_images-defected_images["Good"])*100:.2f}%')

    # Calculate the percentages
    percentages = [(count / (total_images - defected_images['Good'])) * 100 for count in defected_images.values()]


    # Calculate the percentages
    percentages = [(count / (total_images - defected_images['Good'])) * 100 for count in defected_images.values()]

    # Create a bar plot using Seaborn
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=list(defected_images.keys()), y=percentages, palette=['red', 'blue', 'green', 'grey'])
    ax.set_ylabel('Percentage', fontsize=14)
    ax.set_xlabel('Defect Type', fontsize=14)
    ax.set_title('Defected Images by Type', fontsize=16, fontweight='bold')

    # Add text annotations to each bar
    for i, v in enumerate(defected_images.values()):
        ax.text(i, v + 1, str(v), color='black', ha='center', fontsize=12, fontweight='bold')

    # Add a horizontal line at 100%
    ax.axhline(y=100, color='grey', linestyle='--')

    # Display the plot
    plt.show()

