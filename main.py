import pyautogui
import cv2
import numpy as np
import time
from PIL import Image

def capture_screen(region=None):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

def detect_elements(image_rgb):
    # Define color ranges -> Results may vary
    lower_center_color = np.array([177, 197, 0])
    upper_center_color = np.array([217, 237, 20])

    lower_outer_color = np.array([103, 224, 62])
    upper_outer_color = np.array([143, 255, 102])

    # Create masks
    mask_center = cv2.inRange(image_rgb, lower_center_color, upper_center_color)
    mask_outer = cv2.inRange(image_rgb, lower_outer_color, upper_outer_color)

    # Find contours for center and outer masks
    contours_center, _ = cv2.findContours(mask_center, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_outer, _ = cv2.findContours(mask_outer, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Merge contours
    contours = contours_center + contours_outer

    return contours

def isBadColorDetected(image_rgb):
    # Define color range for the specific color (RGB: 176, 36, 198)
    lower_color_endscreen = np.array([176 - 10, 36 - 10, 198 - 10])
    upper_color_endscreen = np.array([176 + 10, 36 + 10, 198 + 10])

    lower_color_startscreen = np.array([250 - 10, 118 - 10, 137 - 10])
    upper_color_startscreen = np.array([250 + 10, 118 + 10, 137 + 10])

    # Create mask for the specific color
    mask_color_endscreen = cv2.inRange(image_rgb, lower_color_endscreen, upper_color_endscreen)

    mask_color_startscreen = cv2.inRange(image_rgb, lower_color_startscreen, upper_color_startscreen)

    # Check if the color is present in the image
    if np.any(mask_color_endscreen) or np.any(mask_color_startscreen):
        return True
    return False

# Get the coordinates of the game window
print("Move the mouse to the top-left corner of the game window and press Enter")
input()
x1, y1 = pyautogui.position()

print("Move the mouse to the bottom-right corner of the game window and press Enter")
input()
x2, y2 = pyautogui.position()

width = x2 - x1
height = y2 - y1

print(f"Game window bounds: ({x1}, {y1}), ({x2}, {y2})")

region = (x1, y1, width, height)

# Main loop to capture screen, detect elements, and click them
while True:
    # Capture screen
    screenshot = capture_screen(region=region)
    
    # Convert to RGB
    image_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    
    # Detect specific color
    if isBadColorDetected(image_rgb):
        continue

    # Detect elements
    contours = detect_elements(image_rgb)
    
    if contours:
        # Sort contours by their y-coordinate (from bottom to top)
        #contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1], reverse=True)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2

            # Click the element
            pyautogui.click(x1 + center_x, y1 + center_y)
            print(f"Clicked element at ({center_x}, {center_y})")

            # Break after clicking the first element from the bottom
            break

