from Crypto.PublicKey import ElGamal
from Crypto import Random
import json
import os

KEYS_DIR = "AppCriptografia/AppCriptografia/keys/elgamal_keys.json"

def generar_y_guardar_claves(bits=2048):
    key = ElGamal.generate(bits, Random.new().read)

    claves = {
        "p": str(key.p),
        "g": str(key.g),
        "y": str(key.y),  # Parte pública
        "x": str(key.x)   # Clave privada
    }

    with open(KEYS_DIR, "w") as f:
        json.dump(claves, f)

    print("Claves guardadas en elgamal_keys.json")


# Llamar una sola vez para generar y guardar las claves
generar_y_guardar_claves()