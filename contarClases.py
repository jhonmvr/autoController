import os
import javalang

# Directorio raíz que contiene los archivos y carpetas de proyecto Java
ROOT_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-modelo\\src\\main\\java\\com\\erp\\dao'

def count_classes_and_interfaces(file_path):
    """Cuenta y devuelve el número de clases y de interfaces en un archivo Java dado."""
    classes_count = 0
    interfaces_count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as java_file:
            content = java_file.read()
        tree = javalang.parse.parse(content)

        # Contar clases
        classes_count += len(list(tree.filter(javalang.tree.ClassDeclaration)))

        # Contar interfaces
        interfaces_count += len(list(tree.filter(javalang.tree.InterfaceDeclaration)))

    except Exception as e:
        print(f"Error al analizar el archivo {file_path}: {e}")

    return classes_count, interfaces_count

def count_classes_recursively(directory):
    """Recorre recursivamente directorios para contar las clases y interfaces Java."""
    total_classes = 0
    total_interfaces = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                classes_count, interfaces_count = count_classes_and_interfaces(file_path)
                print(f"Archivo: {file_path}, Clases: {classes_count}, Interfaces: {interfaces_count}")
                total_classes += classes_count
                total_interfaces += interfaces_count

    return total_classes, total_interfaces

# Contar las clases y las interfaces en el directorio raíz y todos los subdirectorios
total_classes_count, total_interfaces_count = count_classes_recursively(ROOT_DIR)
print(f"Total de clases encontradas: {total_classes_count}")
print(f"Total de interfaces encontradas: {total_interfaces_count}")
