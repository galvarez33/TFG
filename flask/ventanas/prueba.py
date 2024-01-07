import re

def validar_correo(correo):
    # Expresión regular que permite cualquier combinación de caracteres en el nombre de usuario y dominio.
    correo_valido = re.match(r'^.+@.+\..+$', correo)

    return correo_valido is not None

# Ejemplo de uso
correo = 'g.alvarez33@usp.ceu.es'
if validar_correo(correo):
    print(f'La dirección de correo "{correo}" es válida.')
else:
    print(f'La dirección de correo "{correo}" no es válida.')
