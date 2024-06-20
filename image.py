import cv2
import numpy as np

# Load the image
image_path = "C:\\Users\\Mage\\Pictures\\Screenshots\\Screenshot 2024-06-21 011352.png"
image = cv2.imread(image_path)

# Convert the image to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Find the minimum and maximum HSV values
h_min = np.min(hsv_image[:, :, 0])
s_min = np.min(hsv_image[:, :, 1])
v_min = np.min(hsv_image[:, :, 2])

h_max = np.max(hsv_image[:, :, 0])
s_max = np.max(hsv_image[:, :, 1])
v_max = np.max(hsv_image[:, :, 2])

lower_color = np.array([h_min, s_min, v_min])
upper_color = np.array([h_max, s_max, v_max])

print("Lower HSV Bound:", lower_color)
print("Upper HSV Bound:", upper_color)