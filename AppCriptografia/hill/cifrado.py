import numpy as np
def cifrar_hill(mensaje, clave):
    """Lógica para cifrar con el método Hill."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mensaje = mensaje.upper()
    clave = clave.upper()
    resultado = []
    indice_clave = 0

    # Función para convertir letras a números (A=0, B=1, ..., Z=25)
    def letra_a_numero(c):
        return ord(c.upper()) - ord('A')

    # Función para convertir números de vuelta a letras (0=A, 1=B, ..., 25=Z)
    def numero_a_letra(n):
        return chr(n + ord('A'))

    # Paso 1: Parsear la matriz
    # Convertir la cadena de entrada de la matriz (por ejemplo, '5 8 7, 9 1 2, 3 4 6') a una matriz numpy
    matriz = [list(map(int, fila.split())) for fila in clave.split(',')]
    matriz = np.array(matriz)
    tamano_matriz = matriz.shape[0]
    
    # Paso 2: Preparar el texto plano
    # Eliminar caracteres no alfabéticos y convertir a mayúsculas
    mensaje = ''.join([char.upper() for char in mensaje if char.isalpha()])
    
    # Si la longitud del texto plano no es múltiplo de tamano_matriz, rellenarlo con 'X' (se puede elegir otro carácter de relleno)
    while len(mensaje) % tamano_matriz != 0:
        mensaje += 'X'
    
    # Paso 3: Convertir el texto plano a una lista de números
    mensaje_numeros = [letra_a_numero(char) for char in mensaje]
    
    # Paso 4: Cifrar el texto plano usando el cifrado Hill
    # Dividir el texto plano en bloques de tamano_matriz (para que coincida con el tamaño de la matriz)
    resultado_numeros = []
    for i in range(0, len(mensaje_numeros), tamano_matriz):
        bloque = mensaje_numeros[i:i + tamano_matriz]
        bloque_cifrado = np.dot(bloque,matriz) % 26  # Multiplicar la matriz y el bloque, mod 26 para el alfabeto
        print(bloque_cifrado)
        resultado_numeros.extend(bloque_cifrado)
    
    # Paso 5: Convertir los números cifrados de vuelta a letras
    resultado = ''.join([numero_a_letra(num) for num in resultado_numeros])
    
    return resultado


def descifrar_hill(mensaje, clave):
    """Lógica para descifrar con el método Hill."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mensaje = mensaje.upper()
    clave = clave.upper()
    resultado = []
    indice_clave = 0

    for letra in mensaje:
        if letra in alfabeto:
            pos_mensaje = alfabeto.index(letra)
            pos_clave = alfabeto.index(clave[indice_clave % len(clave)])
            nueva_pos = (pos_mensaje - pos_clave) % len(alfabeto)
            resultado.append(alfabeto[nueva_pos])
            indice_clave += 1
        else:
            resultado.append(letra)

    return "".join(resultado)
