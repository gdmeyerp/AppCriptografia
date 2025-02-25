from Crypto.Random import random
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.PublicKey import ElGamal
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta de las claves
ELGAMAL_KEY_PATH = os.path.join(BASE_DIR, "keys", "elgamal_keys.json")

def cargar_claves():
    with open(ELGAMAL_KEY_PATH, "r") as f:
        claves = json.load(f)

    public_key = (int(claves["p"]), int(claves["g"]), int(claves["y"]))
    private_key = (int(claves["p"]), int(claves["g"]), int(claves["x"]))

    return public_key, private_key


# Función para cifrar un mensaje con ElGamal
def elgamal_encrypt(text):
    # Cargar claves desde los archivos json
    public_key, private_key = cargar_claves()

    p, g, y = public_key  # La clave pública contiene (p, g, y)
    
    plaintext_int = bytes_to_long(text.encode())  # Convertir texto a entero
    k = random.StrongRandom().randint(1, p - 2)  # Generar número aleatorio k
    c1 = pow(g, k, p)
    c2 = (plaintext_int * pow(y, k, p)) % p

    return (c1, c2)


# Función para descifrar un mensaje con ElGamal
def elgamal_decrypt(ciphertext):
    # Cargar claves desde los archivos json
    public_key, private_key = cargar_claves()

    p, g, x = private_key  # La clave privada contiene (p, g, x)
    
    c1, c2 = ciphertext
    c1 = int(c1)
    c2 = int(c2) 
    
    s = pow(c1, x, p)  # Clave compartida
    s_inv = pow(s, -1, p)  # Inverso modular
    plaintext_int = (c2 * s_inv) % p  # Recuperar el mensaje

    return long_to_bytes(plaintext_int).decode()  # Convertir entero a texto
