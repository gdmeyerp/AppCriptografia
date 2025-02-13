def cifrar_desplazamiento(mensaje, clave):
    """Cifra el mensaje usando el cifrado César (desplazamiento)."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mensaje = mensaje.upper()
    clave = int(clave)  # Asumimos que la clave es un número entero

    # Función para convertir letras a números (A=0, B=1, ..., Z=25)
    def letra_a_numero(c):
        return ord(c.upper()) - ord('A')

    # Función para convertir números de vuelta a letras (0=A, 1=B, ..., 25=Z)
    def numero_a_letra(n):
        return chr(n + ord('A'))
    
    # Paso 1: Convertir el mensaje a una lista de números
    mensaje_numeros = [letra_a_numero(char) for char in mensaje if char.isalpha()]
    
    # Paso 2: Aplicar el desplazamiento (desplazamiento)
    resultado_numeros = [(num + clave) % 26 for num in mensaje_numeros]
    
    # Paso 3: Convertir los números cifrados de vuelta a letras
    resultado = ''.join([numero_a_letra(num) for num in resultado_numeros])
    
    return resultado


def descifrar_desplazamiento(mensaje, clave):
    """Descifra el mensaje usando el cifrado César (desplazamiento)."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mensaje = mensaje.upper()
    clave = int(clave)

    # Función para convertir letras a números (A=0, B=1, ..., Z=25)
    def letra_a_numero(c):
        return ord(c.upper()) - ord('A')

    # Función para convertir números de vuelta a letras (0=A, 1=B, ..., 25=Z)
    def numero_a_letra(n):
        return chr(n + ord('A'))
    
    # Paso 1: Convertir el mensaje a una lista de números
    mensaje_numeros = [letra_a_numero(char) for char in mensaje if char.isalpha()]
    
    # Paso 2: Aplicar el desplazamiento inverso
    resultado_numeros = [(num - clave) % 26 for num in mensaje_numeros]
    
    # Paso 3: Convertir los números descifrados de vuelta a letras
    resultado = ''.join([numero_a_letra(num) for num in resultado_numeros])
    
    return resultado
