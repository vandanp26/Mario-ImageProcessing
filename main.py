import cv2
import numpy as np
import os

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Load the large image using OpenCV
large_image_path = 'mvp_test.png'  # Assuming mvp_test.png is in the same directory as your script
large_image = cv2.imread(large_image_path)
if large_image is None:
    raise FileNotFoundError(f"Failed to load image: {large_image_path}")

# Load the template image
template_path = 'green_yoshi.png'  # Assuming green_yoshi.png is in the same directory as your script
template = cv2.imread(template_path)
if template is None:
    raise FileNotFoundError(f"Failed to load template image: {template_path}")

# Convert the template to grayscale
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Perform template matching
result = cv2.matchTemplate(cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY), template_gray, cv2.TM_CCOEFF_NORMED)

# Threshold to find matches
threshold = 0.8  # Adjust this threshold as needed
loc = np.where(result >= threshold)

# Draw rectangles around matched areas
for pt in zip(*loc[::-1]):
    cv2.rectangle(large_image, pt, (pt[0] + template_gray.shape[1], pt[1] + template_gray.shape[0]), (0, 255, 0), 2)

# Display the result
cv2.imshow('Yoshi Found', large_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
