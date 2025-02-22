def cifrar_vigenere(mensaje, clave):
    """Lógica para cifrar con el método Vigenère."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mensaje = mensaje.upper()
    clave = clave.upper()
    resultado = []
    indice_clave = 0

    for letra in mensaje:
        if letra in alfabeto:
            pos_mensaje = alfabeto.index(letra)
            pos_clave = alfabeto.index(clave[indice_clave % len(clave)])
            nueva_pos = (pos_mensaje + pos_clave) % len(alfabeto)
            resultado.append(alfabeto[nueva_pos])
            indice_clave += 1
        else:
            resultado.append(letra)

    return "".join(resultado)


def descifrar_vigenere(mensaje, clave):
    """Lógica para descifrar con el método Vigenère."""
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
