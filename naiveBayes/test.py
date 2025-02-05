import numpy as np
import pandas as pd
import cv2
from nb import mean_variance, prior_probs, predict
from PIL import Image

# Load the dataset and prepare the training data
def load_dataset(file_path='D:/DBMS-2/naiveBayes/Skin_NonSkin.txt'):
    column_names = ["R", "G", "B", "Label"]
    df = pd.read_csv(file_path, sep=r'\s+', names=column_names)
    df["Label"] = df["Label"].apply(lambda x: 0 if x == 2 else 1)  # 0 for non-skin, 1 for skin
    X = df[["R", "G", "B"]].values
    y = df["Label"].values
    return X, y

# Train the model with the dataset
def train_model(X, y):
    mean_var = mean_variance(X, y)
    priors = prior_probs(y)
    return mean_var, priors

# Classify a new image using the trained model
def classify_image(image_path, mean_var, priors):
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded. Please check the file path.")
    
    height, width, _ = image.shape
    output_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Flatten the image to process each pixel
    image_flat = image.reshape(-1, 3)

    # Predict class for each pixel (skin or non-skin)
    predictions = predict(image_flat, mean_var, priors)

    # Rebuild the classified image
    for i, pred in enumerate(predictions):
        x, y = divmod(i, width)
        if pred == 1:  # Skin
            output_image[x, y] = image[x, y]
        else:  # Non-skin (black)
            output_image[x, y] = [0, 0, 0]

    return output_image

# Function to calculate skin and non-skin percentages in an image
def calculate_skin_percentage(image_path, mean_var, priors):
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded. Please check the file path.")
    
    height, width, _ = image.shape
    total_pixels = height * width
    skin_pixels = 0

    # Flatten the image to process each pixel
    image_flat = image.reshape(-1, 3)

    # Predict class for each pixel (skin or non-skin)
    predictions = predict(image_flat, mean_var, priors)

    # Count skin pixels
    for pred in predictions:
        if pred == 1:
            skin_pixels += 1

    # Calculate skin and non-skin percentages
    skin_percentage = (skin_pixels / total_pixels) * 100
    non_skin_percentage = 100 - skin_percentage
    print(f"Skin Percentage: {skin_percentage:.2f}%")
    print(f"Non-Skin Percentage: {non_skin_percentage:.2f}%")
    return skin_percentage, non_skin_percentage

# Main function to train and classify the image
def main():
    # Load the dataset and train the model
    X, y = load_dataset()
    mean_var, priors = train_model(X, y)

    # Path to the image you want to classify
    image_path = 'D:/DBMS-2/naiveBayes/skin.jpg'  # Corrected to your actual file name
    output_path = 'classified_output.png'  # Output path for classified image

    # Classify the image and save the output
    output_image = classify_image(image_path, mean_var, priors)
    cv2.imwrite(output_path, output_image)
    print(f"Classified image saved as {output_path}")

    # Calculate skin and non-skin percentages
    calculate_skin_percentage(image_path, mean_var, priors)

if __name__ == "__main__":
    main()