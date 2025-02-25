from Crypto.Cipher import DES
import os
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io
import struct
import numpy as np

def pad_data(data):
    """ Pads data to be multiple of 8 bytes for DES encryption"""
    while len(data) % 8 != 0:
        data += b' ' #Padding with spaces
    return data

def unpad_data(data):
    """ Removes padding from decrypted data"""
    return data.rstrip(b' ')


# Función auxiliar para cifrar una imagen usando DES
def cifrar_imagen_des(input_image_path, output_image_path, clave):

    if len(clave) != 8:
        raise ValueError("Clave DES debe tener exactamente 8 bytes")
    
    # Leer imagen como PNG
    with Image.open(input_image_path) as image_file:
        image_file.save(input_image_path, "PNG")

    with Image.open(input_image_path) as img:
        img.save(output_image_path, "BMP")
        img = img.convert("RGB")
        image_data = np.array(img)

    
    pixel_data = image_data.tobytes()

    # Pad data
    padding_len = 8 - (len(pixel_data) % 8)
    pixel_data += bytes([0] * padding_len)

    # Encriptar con DES
    des_cipher = DES.new(clave.encode(), DES.MODE_CBC)
    encrypted_data = des_cipher.encrypt(pixel_data)

    expected_size = image_data.shape[1] * image_data.shape[0] * 3
    encrypted_array = np.frombuffer(encrypted_data, dtype=np.uint8)
    encrypted_array = encrypted_array[:expected_size]
    encrypted_array = encrypted_array.reshape(image_data.shape)

    encrypted_image = Image.fromarray(encrypted_array)
    encrypted_image.save(output_image_path, "BMP")
    return output_image_path

# Función auxiliar para descifrar una imagen usando DES
def descifrar_imagen_des(input_image_path, output_image_path, clave):

    if len(clave) != 8:
        raise ValueError("Clave DES debe tener exactamente 8 bytes")
    
    # Leer imagen como binario
    with open(input_image_path, 'rb') as image_file:
        image_data = image_file.read()


    # Descifrar con DES
    des_cipher = DES.new(clave.encode(), DES.MODE_ECB)
    decrypted_data = des_cipher.decrypt(image_data)

    # Quitar padding
    cleaned_data = unpad_data(decrypted_data)

    # Guardar imagen encriptada
    with open(output_image_path, 'wb') as decrypted_file:
        decrypted_file.write(cleaned_data)
    
    return output_image_path

def cifrar_imagen_des_raster(input_image_path, output_image_path, key):
    if isinstance(key, str):
        key = key.encode('utf-8')  # Convert key to bytes (if it's a string)
    key = key[:8]  # Truncate to 8 bytes (if longer)
    key = key.ljust(8, b'\0')  # Pad to 8 bytes (if shorter)

    # Ensure the key is 8 bytes (DES key length)
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long.")
    
    # Open the image using Pillow
    with Image.open(input_image_path) as img:
        # Extract width and height
        width, height = img.size

        # Convert image to raw byte data (raster data)
        img_bytes = img.tobytes()

    # Create DES cipher object in CBC mode
    cipher = DES.new(key, DES.MODE_CBC)

    # Pad the image data to make it a multiple of DES block size (8 bytes)
    padded_data = pad(img_bytes, DES.block_size)

    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)

    # Save the encrypted data along with the IV at the beginning
    with open(output_image_path, 'wb') as out_file:
        # Write the IV first (needed for decryption)
        out_file.write(cipher.iv)

        # Write the width and height (store them as 4-byte unsigned integers)
        out_file.write(struct.pack('!II', width, height))  # Correct usage of struct.pack

        # Write the encrypted raster data
        out_file.write(encrypted_data)
    
    return output_image_path

def descifrar_imagen_des_raster(input_encrypted_image_path, output_image_path, key):

    if isinstance(key, str):
        key = key.encode('utf-8')  # Convert key to bytes (if it's a string)
    key = key[:8]  # Truncate to 8 bytes (if longer)
    key = key.ljust(8, b'\0')  # Pad to 8 bytes (if shorter)

    # Ensure the key is 8 bytes (DES key length)
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long.")
    
    # Read the encrypted image data
    with open(input_encrypted_image_path, 'rb') as enc_file:
        # The first 8 bytes are the IV
        iv = enc_file.read(8)

        # The next 8 bytes are the width and height
        width, height = struct.unpack('!II', enc_file.read(8))
        # The rest is the encrypted raster data
        encrypted_data = enc_file.read()

    # Create DES cipher object using the IV
    cipher = DES.new(key, DES.MODE_CBC, iv)

    # Decrypt the data
    decrypted_data = unpad(cipher.decrypt(encrypted_data), DES.block_size)

    # Convert decrypted bytes back into an image
    img = Image.frombytes('RGB', (width, height), decrypted_data)  # Specify image dimensions here
    img.save(output_image_path)
    
    return output_image_path