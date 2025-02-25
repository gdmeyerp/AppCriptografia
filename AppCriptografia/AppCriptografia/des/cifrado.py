from Crypto.Cipher import DES
import os

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
    
    # Leer imagen como binario
    with open(input_image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Pad data
    padded_data = pad_data(image_data)

    # Encriptar con DES
    des_cipher = DES.new(clave.encode(), DES.MODE_ECB)
    encrypted_data = des_cipher.encrypt(padded_data)

    # Guardar imagen encriptada
    with open(output_image_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    
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
        decrypted_file.write(decrypted_data)
    
    return output_image_path
