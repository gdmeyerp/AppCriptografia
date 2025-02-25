import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class ECCrypto:
    """
    Clase para manejar cifrado y descifrado usando ECC y AES-GCM.
    """

    def __init__(self, curva=ec.SECP256R1()):
        self.curva = curva

    def generar_claves(self):
        """
        Genera un par de claves ECC (privada y pública) en formato PEM.
        """
        clave_privada = ec.generate_private_key(self.curva)
        clave_publica = clave_privada.public_key()

        privada_pem = clave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        publica_pem = clave_publica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return privada_pem, publica_pem

    @staticmethod
    def cifrar(clave_publica_pem, mensaje):
        """
        Cifra un mensaje con la clave pública.
        """
        clave_publica = serialization.load_pem_public_key(clave_publica_pem.encode())

        clave_efimera = ec.generate_private_key(ec.SECP256R1())
        secreto_compartido = clave_efimera.exchange(ec.ECDH(), clave_publica)

        clave_derivada = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'ecdh handshake'
        ).derive(secreto_compartido)

        iv = os.urandom(12)
        cifrador = Cipher(algorithms.AES(clave_derivada), modes.GCM(iv))
        encriptador = cifrador.encryptor()
        mensaje_cifrado = encriptador.update(mensaje.encode()) + encriptador.finalize()

        clave_efimera_pem = clave_efimera.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return clave_efimera_pem.decode(), iv.hex(), encriptador.tag.hex(), mensaje_cifrado.hex()

    @staticmethod
    def descifrar(clave_privada_pem, clave_efimera_pem, iv, etiqueta, mensaje_cifrado):
        """
        Descifra un mensaje usando la clave privada y la clave efímera.
        """
        clave_privada = serialization.load_pem_private_key(clave_privada_pem.encode(), password=None)
        clave_efimera = serialization.load_pem_public_key(clave_efimera_pem.encode())

        secreto_compartido = clave_privada.exchange(ec.ECDH(), clave_efimera)

        clave_derivada = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'ecdh handshake'
        ).derive(secreto_compartido)

        cifrador = Cipher(algorithms.AES(clave_derivada), modes.GCM(bytes.fromhex(iv), bytes.fromhex(etiqueta)))
        desencriptador = cifrador.decryptor()
        mensaje_descifrado = desencriptador.update(bytes.fromhex(mensaje_cifrado)) + desencriptador.finalize()

        return mensaje_descifrado.decode()
