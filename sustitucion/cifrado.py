def cifrar_sustitucion(mensaje, permutacion_string):
    try:
        mensaje_min = mensaje.lower().replace(' ', '')
        mensaje_num = []
        for i in mensaje_min:
            mensaje_num.append(ord(i)-97)
        mensaje_permutado_num = []
        permutacion = permutacion_string.split(',')
        for i in mensaje_num:
            mensaje_permutado_num.append(permutacion[i])
        mensaje_cod_num = []
        for i in mensaje_permutado_num:
            mensaje_cod_num.append(chr(97 + int(i)))
        mensaje_cod = ''.join(mensaje_cod_num)
        return mensaje_cod
    except Exception as e:
        raise ValueError(f"Error al cifrar: {e}")

def decifrar_sustitucion(mensaje, permutacion_string):
    try:
        mensaje_min = mensaje.lower().replace(' ', '')
        mensaje_num = []
        for i in mensaje_min:
            mensaje_num.append(ord(i)-97)
        mensaje_permutado_num = []
        permutacion = permutacion_string.split(',')
        permutacion_int = []
        for elem in permutacion:
            permutacion_int.append(int(elem))
        print(permutacion_int)
        for i in mensaje_num:
            mensaje_permutado_num.append(permutacion_int.index(i))
        mensaje_decod_num = []
        for i in mensaje_permutado_num:
            mensaje_decod_num.append(chr(97 + int(i)))
        mensaje_decod = ''.join(mensaje_decod_num)
        return mensaje_decod
    except Exception as e:
        raise ValueError(f"Error al decifrar: {e}")
