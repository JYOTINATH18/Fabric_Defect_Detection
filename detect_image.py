import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

def detect_defect(new_image_path):
    # Load the saved model
    model = tf.keras.models.load_model('fabric_defect_model.h5')

    # Load the new image
    new_image = cv2.imread(new_image_path)
    new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    # convert to RGB format
    original_image = new_image.copy()  # save a copy of the original image

    # Preprocess the image
    new_image = cv2.resize(new_image, (224, 224))  # resize to match VGG16 input size
    new_image = np.expand_dims(new_image, axis=0)  # add batch dimension

    # Classify the image
    predictions = model.predict(new_image)
    predicted_class = np.argmax(predictions)

    # Get the class label
    classes = ['Good', 'Hole', 'Lines', 'Stain']
    predicted_label = classes[predicted_class]

    print(f"Predicted defect type: {predicted_label}")

    img = cv2.imread(new_image_path)

    # Convert the image to grayscale
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
    print(f"Percentage of defected area: {percentage_defected_area:.2f}%")
    # Draw rectangles around the defects
    for defect in defects:
        x, y, w, h = defect
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Add text to the image indicating the predicted defect type and percentage of defected area
    text = f"Defect type: {predicted_label}"
    text2 = f"Percentage of defected area: {percentage_defected_area:.2f}%"

    # Display the image
    # Define the position and style of the text areas
    text_pos1 = (0, 0)
    text_style1 = dict(facecolor='yellow', alpha=0.9)

    text_pos2 = (0, 120)
    text_style2 = dict(facecolor='yellow', alpha=0.9)

    # Display the image
    plt.imshow(img)

    # Add the text areas to the image
    plt.text(*text_pos1, text, color='blue', bbox=text_style1)
    plt.text(*text_pos2, text2, color='blue', bbox=text_style2)

    # Hide the axis
    plt.axis('off')

    # Show the window
    plt.show()




