from PIL import Image
import numpy as np

def extract_message(image_array):
    message_bits = []
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            message_bits.append(image_array[i, j] & 1)  # Extract the LSB of each pixel

    message_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(message_bits):
                byte |= (message_bits[i + j] << j)
        message_bytes.append(byte)
        # Stop processing when the end of the message symbol (null byte) is encountered
        if message_bytes[-1] == 0:
            break

    hidden_message = message_bytes.decode("utf-8", errors="ignore")

    return hidden_message.rstrip("\x00")  # Remove trailing null bytes

def reconstruct_image(shares_paths):
    try:
        shares = [np.array(Image.open(path).convert("L")) for path in shares_paths]
        reconstructed_image = shares[0].copy()

        for share in shares[1:]:
            reconstructed_image = np.bitwise_xor(reconstructed_image, share)

        return reconstructed_image

    except Exception as e:
        print(f"Error during image reconstruction: {e}")
        return None

# Example usage:
shares_paths = [
    "Project_image_share_1.png",
    "Project_image_share_2.png",
    "Project_image_share_3.png",
    "Project_image_share_4.png",
    "Project_image_share_5.png",
    "Project_image_share_6.png",
    "Project_image_share_7.png",
    "Project_image_share_8.png",
    "Project_image_share_9.png",
    "Project_image_share_10.png",
]

# Reconstruct the image
reconstructed_image = reconstruct_image(shares_paths)

if reconstructed_image is not None:
    # Extract the hidden message from the reconstructed image
    hidden_message = extract_message(reconstructed_image)

    # Save the reconstructed image as "constructed.png"
    Image.fromarray(reconstructed_image.astype(np.uint8)).save("constructed.png")
    print("Reconstructed image saved as 'constructed.png'.")
    print("Hidden Message:", hidden_message)
else:
    print("Failed to reconstruct the image.")
