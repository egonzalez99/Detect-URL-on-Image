import pyautogui
import time

# Define the image you want to search for
image_path = 'C:\Users\geddi\Downloads\image.jpg'

# Search for the image on the screen
image_location = pyautogui.locateOnScreen(image_path, confidence=0.8)

if image_location:
    # Image found, get the center coordinates
    x, y, width, height = image_location
    # Define a region of interest (x, y, width, height) 
    region = (x, y, width, height)
    image_location = pyautogui.locateOnScreen(image_path, region=region, confidence=0.8)
    center_x = x + width // 2
    center_y = y + height // 2
    print(f"The image was found at coordinates ({center_x}, {center_y})!")
else:
    print("The image was not found.")