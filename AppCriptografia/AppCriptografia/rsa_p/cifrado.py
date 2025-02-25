from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generar_claves():
    """
    Genera un par de claves RSA (pública y privada).
    Retorna las claves en formato string.
    """
    key = RSA.generate(2048)  # Genera un par de claves de 2048 bits
    clave_privada = key.export_key()  # Clave privada
    clave_publica = key.publickey().export_key()  # Clave pública
    return clave_publica.decode(), clave_privada.decode()

def cifrar_rsa(mensaje, clave_publica):
    """
    Cifra un mensaje utilizando una clave pública RSA.
    - mensaje: texto plano a cifrar (string).
    - clave_publica: clave pública RSA (string).
    Retorna el mensaje cifrado como un string codificado en base64.
    """
    try:
        key = RSA.import_key(clave_publica)  # Importa la clave pública
        cipher = PKCS1_OAEP.new(key)  # Inicializa el cifrado
        mensaje_cifrado = cipher.encrypt(mensaje.encode())  # Cifra el mensaje
        return base64.b64encode(mensaje_cifrado).decode()  # Codifica en base64
    except Exception as e:
        raise ValueError(f"Error al cifrar: {e}")

def descifrar_rsa(mensaje_cifrado, clave_privada):
    """
    Descifra un mensaje cifrado utilizando una clave privada RSA.
    - mensaje_cifrado: texto cifrado en base64 (string).
    - clave_privada: clave privada RSA (string).
    Retorna el mensaje descifrado como un string.
    """
    try:
        key = RSA.import_key(clave_privada)  # Importa la clave privada
        cipher = PKCS1_OAEP.new(key)  # Inicializa el descifrado
        mensaje_descifrado = cipher.decrypt(base64.b64decode(mensaje_cifrado))  # Descifra el mensaje
        return mensaje_descifrado.decode()  # Decodifica el mensaje
    except Exception as e:
        raise ValueError(f"Error al descifrar: {e}")
