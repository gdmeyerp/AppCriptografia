import numpy as np
import math

def cifrar_afin(mensaje, a, b):
    """Lógica para cifrar con el método Afin."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    m = len(alfabeto)  # Tamaño del alfabeto (26)

    # Validar que 'a' y 'm' sean coprimos
    if math.gcd(a, m) != 1:
        raise ValueError("'a' debe ser coprimo con 26 para que el cifrado funcione.")

    # Convertir mensaje a mayúsculas y eliminar caracteres no alfabéticos
    mensaje = ''.join([char.upper() for char in mensaje if char.isalpha()])

    # Función para convertir letras a números (A=0, B=1, ..., Z=25)
    def letra_a_numero(c):
        return ord(c.upper()) - ord('A')

    # Función para convertir números de vuelta a letras (0=A, 1=B, ..., 25=Z)
    def numero_a_letra(n):
        return chr(n + ord('A'))

    # Aplicar la fórmula de cifrado: C = (a * P + b) % 26
    resultado = ''.join([numero_a_letra((a * letra_a_numero(char) + b) % m) for char in mensaje])

    return resultado

def descifrar_afin(mensaje, a, b):
    """Lógica para descifrar con el método Afin."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    m = len(alfabeto)  # Tamaño del alfabeto (26)

    # Validar que 'a' y 'm' sean coprimos
    if math.gcd(a, m) != 1:
        raise ValueError("'a' debe ser coprimo con 26 para que el descifrado funcione.")

    # Convertir mensaje a mayúsculas y eliminar caracteres no alfabéticos
    mensaje = ''.join([char.upper() for char in mensaje if char.isalpha()])

    # Función para convertir letras a números (A=0, B=1, ..., Z=25)
    def letra_a_numero(c):
        return ord(c.upper()) - ord('A')

    # Función para convertir números de vuelta a letras (0=A, 1=B, ..., 25=Z)
    def numero_a_letra(n):
        return chr(n + ord('A'))

    # Calcular el inverso modular de 'a' módulo 26
    def inverso_modular(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError(f"No se encontró el inverso modular para a = {a} y m = {m}.")

    a_inverso = inverso_modular(a, m)

    # Aplicar la fórmula de descifrado: P = a^(-1) * (C - b) % 26
    resultado = ''.join([numero_a_letra((a_inverso * (letra_a_numero(char) - b)) % m) for char in mensaje])

    return resultado