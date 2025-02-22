def gcd(p, q):
    while q != 0:
        p, q = q, p % q
    return p

def is_coprime(x, y):
    return gcd(x, y) == 1

def get_inverse(x):
    if x == 7:
        return 15
    elif x == 15:
        return 7
    elif x == 11:
        return 19
    elif x == 19:
        return 11
    else:
        raise ValueError('La clave ingresada no puede ser usada para decifrar el mensaje.')

def cifrar_multiplicativo(mensaje, clave):
    try:
        clave = int(clave)
        if is_coprime(clave, 26) is False:
            raise ValueError('La clave ingresada no puede ser usada para cifrar el mensaje.')
        mensaje_min = mensaje.lower().replace(' ', '')
        mensaje_num = []
        for i in mensaje_min:
            mensaje_num.append(ord(i)-97)
        mensaje_multi_num = []
        for i in mensaje_num:
            mensaje_multi_num.append((i*clave) % 26)
        mensaje_cod_num = []
        for i in mensaje_multi_num:
            mensaje_cod_num.append(chr(97 + int(i)))
        mensaje_cod = ''.join(mensaje_cod_num)
        return mensaje_cod
    except Exception as e:
        raise ValueError(f"Error al cifrar: {e}")

def decifrar_multiplicativo(mensaje, clave):
    try:
        clave = int(clave)
        clave_inv = get_inverse(clave)
        if is_coprime(clave, 26) is False:
            raise ValueError('La clave ingresada no puede ser usada para descifrar el mensaje.')
        mensaje_min = mensaje.lower().replace(' ', '')
        mensaje_num = []
        for i in mensaje_min:
            mensaje_num.append(ord(i)-97)
        mensaje_demulti_num = []
        for i in mensaje_num:
            mensaje_demulti_num.append((i*clave_inv) % 26)
        mensaje_decod_num = []
        for i in mensaje_demulti_num:
            mensaje_decod_num.append(chr(97 + int(i)))
        mensaje_decod = ''.join(mensaje_decod_num)
        return mensaje_decod
    except Exception as e:
        raise ValueError(f"Error al decifrar: {e}")
