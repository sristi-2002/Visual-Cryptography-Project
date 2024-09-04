from PIL import Image
import numpy as np

def embed_message(image_array, message):
    # Convert the message to a byte array
    message_bytes = message.encode("utf-8")

    # Get the dimensions of the image
    height, width = image_array.shape

    # Check if the image is large enough to embed the message
    if len(message_bytes) * 8 > height * width:
        raise ValueError("Message is too long to be embedded in the image.")

    # Embed the message into the LSB (Least Significant Bit) of the image array
    byte_idx = 0
    bit_idx = 0
    for byte in message_bytes:
        for j in range(8):  # Iterate over each bit in the byte
            bit = (byte >> j) & 1  # Extract the j-th bit from the byte
            # Embed the bit into the least significant bit of the image pixel
            image_array[byte_idx, bit_idx] = (image_array[byte_idx, bit_idx] & 254) | bit  # Set the LSB of image pixel to bit
            bit_idx += 1
            if bit_idx >= width:
                bit_idx = 0
                byte_idx += 1

    return image_array

def generate_shares(image_path, num_shares, message):
    try:
        # Open and convert the image to grayscale
        original_image = Image.open(image_path).convert("L")
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Convert the image to a NumPy array
    image_array = np.array(original_image)

    # Embed the message into the image array
    try:
        image_array = embed_message(image_array, message)
    except ValueError as e:
        print(f"Error embedding message: {e}")
        return

    # Initialize a list to store the shares
    shares = []

    # Create num_shares - 1 random binary matrices
    for _ in range(num_shares - 1):
        random_matrix = np.random.randint(0, 256, size=image_array.shape, dtype=np.uint8)
        shares.append(random_matrix)

    # Compute the last share such that XORing all shares will give the original image with message
    last_share = image_array.copy()
    for share in shares:
        last_share = np.bitwise_xor(last_share, share)
    shares.append(last_share)

    # Save the shares as image files
    for i, share in enumerate(shares):
        share_image = Image.fromarray(share)
        share_image.save(f"Project_image_share_{i + 1}.png")  # Save each share as an image file

    print(f"{num_shares} shares generated successfully with embedded message: '{message}'.")

def take_input():
    num_shares = int(input("Enter the number of shares: "))
    message = input("Enter the message to hide in the shares: ")
    return num_shares, message

# Example usage:
original_image_path = "D:\\sristi pendrive\\PROJECTS\\CN VISUAL CRYPTROGRAPHY\\tiger_new.png"  # Ensure this file exists in the directory
# original_image_path = "D:\\sristi pendrive\\PROJECTS\\CN VISUAL CRYPTROGRAPHY\\pic1.png" 
num_shares, message_to_hide = take_input()

# Generate shares with embedded message
generate_shares(original_image_path, num_shares, message_to_hide)










# from PIL import Image
# import numpy as np


# def embed_message(image_array, message):
#     # Convert the message to a byte array
#     message_bytes = message.encode("utf-8")

#     # Get the dimensions of the image
#     height, width = image_array.shape

#     # Embed the message into the LSB (Least Significant Bit) of the image array
#     for i, byte in enumerate(message_bytes):
#         for j in range(8):  # Iterate over each bit in the byte
#             bit = (byte >> j) & 1  # Extract the j-th bit from the byte
#             # Embed the bit into the least significant bit of the image pixel
#             image_array[i, j] = (
#                 image_array[i, j] & 254
#             ) | bit  # Set the LSB of image pixel to bit

#     return image_array


# def generate_shares(image_path, num_shares, message):
#     # Open and convert the image to grayscale
#     original_image = Image.open(image_path).convert("L")
#     # Convert the image to a NumPy array
#     image_array = np.array(original_image)

#     # Get the dimensions of the image
#     height, width = image_array.shape

#     # Embed the message into the image array
#     image_array = embed_message(image_array, message)

#     # Initialize a list to store the shares
#     shares = []

#     # Create num_shares - 1 random binary matrices
#     for _ in range(num_shares - 1):
#         random_matrix = np.random.randint(0, 256, size=(height, width), dtype=np.uint8)
#         shares.append(random_matrix)

#     # Compute the last share such that XORing all shares will give the original image with message
#     last_share = image_array.copy()
#     for share in shares:
#         last_share = np.bitwise_xor(last_share, share)
#     shares.append(last_share)

#     # Save the shares as image files
#     for i, share in enumerate(shares):
#         share_image = Image.fromarray(share)
#         share_image.save(
#             f"Project_image_share_{i + 1}.png"
#         )  # Save each share as an image file

#     print(
#         f"{num_shares} shares generated successfully with embedded message: '{message}'."
#     )


# # Function to take mass message input
# def take_mass_message_input():
#     message = input("Enter the message to hide in the shares: ")
#     return message


# # Example usage:
# original_image_path = "tiger_new.png"  # Ensure this file exists in the directory
# num_shares = 5

# # Take input for the message to hide in shares
# message_to_hide = take_mass_message_input()

# # Generate shares with embedded message
# generate_shares(original_image_path, num_shares, message_to_hide)
