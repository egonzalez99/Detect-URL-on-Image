from PIL import Image
#Edward Gonzalez
#extract the data info based on the width and height of the image
def extract_text(image_path):
    img = Image.open(image_path)
    width, height = img.size
    data = list(img.getdata())

    binary = ""
    for x, y, z in data:
        binary += bin(x)[-1]
        binary += bin(y)[-1]
        binary += bin(z)[-1]
    #loop through the length of the data and outputs it into a text format for the user
    secretText = ""
    for i in range(0, len(binary), 10):
        secretText += chr(int(binary[i:i + 10], 2))

    return secretText


# Example usage (modified for extraction only)
imagePath = "encoded_image.jpg"  # Assuming the image with hidden text

# Extract the hidden text from the image
extracted = extract_text(imagePath)
print("Extracted text:", extracted)