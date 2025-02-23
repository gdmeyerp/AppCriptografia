# Archivo para generar las claves RSA que se usan en la firma digital de Documentos

from Crypto.PublicKey import RSA
import os

KEYS_DIR = "AppCriptografia/AppCriptografia/keys"
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "rsa_private.pem")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "rsa_public.pem")

def generate_keys():
    if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)

    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        with open(PRIVATE_KEY_PATH, "wb") as priv_file:
            priv_file.write(private_key)

        with open(PUBLIC_KEY_PATH, "wb") as pub_file:
            pub_file.write(public_key)

        print("🔐 Claves generadas y almacenadas en 'keys/'.")
    else:
        print("✅ Las claves ya existen.")

# Ejecutar solo una vez
generate_keys()
