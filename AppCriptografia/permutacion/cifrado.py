import numpy as np
def cifrar_permutacion(mensaje, clave):
    """Lógica para cifrar con el método de Permutación."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mensaje = mensaje.upper()
    clave = clave.upper()

    # Función para convertir letras a números (A=0, B=1, ..., Z=25)
    def letra_a_numero(c):
        return ord(c.upper()) - ord('A')

    # Función para convertir números de vuelta a letras (0=A, 1=B, ..., 25=Z)
    def numero_a_letra(n):
        return chr(n + ord('A'))
    
    # Paso 1: Parsear la permutación
    # Convertir la cadena de permutación en una lista de enteros
    permutacion = list(map(int, clave.split()))
    tamano_permutacion = len(permutacion)  # Tamaño de la permutación (número de elementos)
    
    # Paso 2: Preparar el texto plano
    # Eliminar caracteres no alfabéticos y convertir a mayúsculas
    mensaje = ''.join([char.upper() for char in mensaje if char.isalpha()])
    
    # Si la longitud del texto plano no es múltiplo de tamano_permutacion, rellenarlo con 'X' (se puede elegir otro carácter de relleno)
    while len(mensaje) % tamano_permutacion != 0:
        mensaje += 'X'
    
    # Paso 3: Convertir el texto plano a una lista de números
    mensaje_numeros = [letra_a_numero(char) for char in mensaje]
    
    resultado_numeros = []
    # Recorrer el texto plano en bloques del tamaño de la permutación
    for i in range(0, len(mensaje_numeros), tamano_permutacion):
        bloque = mensaje_numeros[i:i + tamano_permutacion]
        
        # Aplicar la permutación: reorganizar los caracteres según la lista de permutación
        bloque_cifrado = [0] * tamano_permutacion
        for j in range(tamano_permutacion):
            # La permutación define a qué posición debe ir cada carácter
            # Restamos 1 a cada índice de la permutación para ajustarlo al índice de Python
            bloque_cifrado[j] = bloque[permutacion[j] - 1]
        
        # Aplanar el bloque cifrado y agregarlo al resultado
        resultado_numeros.extend(bloque_cifrado)
    
    # Paso 5: Convertir los números cifrados de vuelta a letras
    resultado = ''.join([numero_a_letra(num) for num in resultado_numeros])
    
    return resultado


def descifrar_permutacion(mensaje, clave):
    """Lógica para cifrar con el método de Permutación."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mensaje = mensaje.upper()
    clave = clave.upper()

    # Función para convertir letras a números (A=0, B=1, ..., Z=25)
    def letra_a_numero(c):
        return ord(c.upper()) - ord('A')

    # Función para convertir números de vuelta a letras (0=A, 1=B, ..., 25=Z)
    def numero_a_letra(n):
        return chr(n + ord('A'))
    
    # Paso 1: Parsear la permutación
    # Convertir la cadena de permutación en una lista de enteros
    permutacion = list(map(int, clave.split()))
    tamano_permutacion = len(permutacion)  # Tamaño de la permutación (número de elementos)
    
    # Paso 2: Preparar el texto plano
    # Eliminar caracteres no alfabéticos y convertir a mayúsculas
    mensaje = ''.join([char.upper() for char in mensaje if char.isalpha()])
    
    # Si la longitud del texto plano no es múltiplo de tamano_permutacion, rellenarlo con 'X' (se puede elegir otro carácter de relleno)
    while len(mensaje) % tamano_permutacion != 0:
        mensaje += 'X'
    
    # Paso 3: Convertir el texto plano a una lista de números
    mensaje_numeros = [letra_a_numero(char) for char in mensaje]
    
    resultado_numeros = []
    # Recorrer el texto plano en bloques del tamaño de la permutación
    for i in range(0, len(mensaje_numeros), tamano_permutacion):
        bloque = mensaje_numeros[i:i + tamano_permutacion]
        
        # Aplicar la permutación: reorganizar los caracteres según la lista de permutación
        bloque_cifrado = [0] * tamano_permutacion
        for j in range(tamano_permutacion):
            # La permutación define a qué posición debe ir cada carácter
            # Restamos 1 a cada índice de la permutación para ajustarlo al índice de Python
            bloque_cifrado[j] = bloque[permutacion[j] - 1]
        
        # Aplanar el bloque cifrado y agregarlo al resultado
        resultado_numeros.extend(bloque_cifrado)
    
    # Paso 5: Convertir los números cifrados de vuelta a letras
    resultado = ''.join([numero_a_letra(num) for num in resultado_numeros])
    
    return resultado