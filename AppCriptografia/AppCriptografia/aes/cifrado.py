from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

def cifrar_imagen_aes(input_image_path, output_image_path, clave):
    """
    Encrypts an image using AES (supports 16, 24, or 32-byte keys).

    Args:
        input_image_path (str): Path to the original image.
        output_image__path (str): Path where the encrypted image will be saved.
        clave (str): Key for AES encryption (must be 16, 24, or 32 bytes).
    """
    key_length = len(clave)
    if key_length not in [16, 24, 32]:
        raise ValueError("Clave AES debe tener  16, 24, o 32 bytes.")

    # Read the image as binary
    with open(input_image_path, 'rb') as img_file:
        image_data = img_file.read()

    # Generate a random IV (16 bytes)
    iv = os.urandom(16)

    # Create AES cipher in CBC mode
    cipher = AES.new(clave.encode(), AES.MODE_CBC, iv)

    # Encrypt the image data with padding
    encrypted_data = cipher.encrypt(pad(image_data, AES.block_size))

    # Save the IV + encrypted image
    with open(output_image_path, 'wb') as encrypted_file:
        encrypted_file.write(iv + encrypted_data)  # Prepend IV for decryption

    return output_image_path

from Crypto.Util.Padding import unpad

def descifrar_imagen_aes(input_image_path, output_image_path, clave):
    """
    Decrypts an AES-encrypted image and restores it to its original format.

    Args:
        input_image_path (str): Path to the encrypted image.
        output_image_path (str): Path where the decrypted image will be saved.
        clave (str): Key for AES decryption (must be 16, 24, or 32 bytes).
    """
    key_length = len(clave)
    if key_length not in [16, 24, 32]:
        raise ValueError("Clave AES debe tener  16, 24, o 32 bytes.")

    # Read encrypted data
    with open(input_image_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Extract IV (first 16 bytes) and encrypted image data
    iv = encrypted_data[:16]
    encrypted_image_data = encrypted_data[16:]

    # Create AES cipher in CBC mode with extracted IV
    cipher = AES.new(clave.encode(), AES.MODE_CBC, iv)

    # Decrypt and remove padding
    decrypted_data = unpad(cipher.decrypt(encrypted_image_data), AES.block_size)

    # Save decrypted image
    with open(output_image_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    return output_image_path