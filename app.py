from PIL import Image


def embed_text(image_path, secret_text, output_path, mode="hide"):
    img = Image.open(image_path)
    width, height = img.size

    data = list(img.getdata())
    binary_secret = ''.join(format(ord(char), '08b') for char in secret_text)

    if len(binary_secret) > len(data) * 3 and mode == "hide":
        raise ValueError("Text too long to be encoded")

    data_index = 0
    for i in range(len(data)):
        r, g, b = data[i]
        # Modify LSB based on mode (hide or extract)
        r = (r & 0b11111110) | (int(binary_secret[data_index]) if mode == "hide" else (r & 1))
        data_index += 1
        g = (g & 0b11111110) | (int(binary_secret[data_index]) if mode == "hide" else (g & 1))
        data_index += 1
        b = (b & 0b11111110) | (int(binary_secret[data_index]) if mode == "hide" else (b & 1))
        data_index += 1
        data[i] = (r, g, b)

    img.putdata(data)
    img.save(output_path)

# extract any text hidden/embedded inside the image
def extract_text(image_path):
    img = Image.open(image_path)
    width, height = img.size
    data = list(img.getdata())
    # looks for binary hidden
    binary_secret = ""
    for r, g, b in data:
        binary_secret += bin(r)[-1]
        binary_secret += bin(g)[-1]
        binary_secret += bin(b)[-1]

    secret_text = ""
    for i in range(0, len(binary_secret), 10):
        secret_text += chr(int(binary_secret[i:i + 10], 2))

    return secret_text


# Example usage
image_path = "image.jpg"
secret_text = "Hello, this is a secret message!"
output_path = "encoded_image.jpg"

# Hide the secret text in the image
embed_text(image_path, secret_text, output_path)

# Extract the hidden text from the image
extracted_text = extract_text(output_path)
print("Extracted text:", extracted_text)