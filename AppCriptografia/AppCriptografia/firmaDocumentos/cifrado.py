from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta de las claves
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "keys", "rsa_private.pem")
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "keys", "rsa_public.pem")

def cargar_claves():
    """Carga la clave privada y pública desde los archivos en /keys/"""
    with open(PRIVATE_KEY_PATH, "rb") as priv_file:
        private_key = RSA.import_key(priv_file.read())

    with open(PUBLIC_KEY_PATH, "rb") as pub_file:
        public_key = RSA.import_key(pub_file.read())

    return private_key, public_key

# Llamada a la función para obtener las claves
PRIVATE_KEY, PUBLIC_KEY = cargar_claves()

def sign_doc(archivo):
    # Leer contenido del archivo
    contenido = archivo.read()

    # Crear hash y firmar
    hash_obj = SHA256.new(contenido)
    firma = pkcs1_15.new(PRIVATE_KEY).sign(hash_obj)

    # Nombre del archivo de firma
    firma_path = f"{archivo.name}.sig"

    # Guardar la firma en un archivo separado
    with open(firma_path, "wb") as f:
        f.write(firma)

    return firma_path


def validate_sign(archivo, firma):
    # Leer contenido del archivo
    contenido = archivo.read()

    # Leer la firma
    firma = firma.read()

    # Verificar la firma
    hash_obj = SHA256.new(contenido)
    try:
        pkcs1_15.new(PUBLIC_KEY).verify(hash_obj, firma)
        return True
    except (ValueError, TypeError):
        return False
    
