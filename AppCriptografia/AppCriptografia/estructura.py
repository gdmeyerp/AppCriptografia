import os

def listar_estructura(directorio, nivel=0):
    # Itera sobre los archivos y directorios dentro de la carpeta actual
    for elemento in sorted(os.listdir(directorio)):
        ruta = os.path.join(directorio, elemento)
        print("│   " * nivel + "├── " + elemento)
        # Si es un directorio, llama recursivamente
        if os.path.isdir(ruta):
            listar_estructura(ruta, nivel + 1)

if __name__ == "__main__":
    directorio_base = os.path.dirname(os.path.abspath(__file__))  # Cambia si necesitas otra carpeta base
    print(f"Estructura de {directorio_base}:\n")
    listar_estructura(directorio_base)
