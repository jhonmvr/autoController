import os
import javalang

# Directorio raíz que contiene los archivos y carpetas de proyecto Java
ROOT_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\gestor'

def count_methods_and_interfaces(file_path):
    """Cuenta y devuelve el número de métodos en clases y en interfaces de un archivo Java dado."""
    methods_count = 0
    interface_methods_count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as java_file:
            content = java_file.read()
        tree = javalang.parse.parse(content)

        # Contar métodos en clases
        for _, class_node in tree.filter(javalang.tree.ClassDeclaration):
            methods_count += sum(1 for _ in class_node.methods)

        # Contar métodos en interfaces
        for _, interface_node in tree.filter(javalang.tree.InterfaceDeclaration):
            interface_methods_count += sum(1 for _ in interface_node.methods)

    except Exception as e:
        print(f"Error al analizar el archivo {file_path}: {e}")

    return methods_count, interface_methods_count

def count_methods_recursively(directory):
    """Recorre recursivamente directorios para contar los métodos de las clases y interfaces Java."""
    total_methods = 0
    total_interface_methods = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                methods_count, interface_methods_count = count_methods_and_interfaces(file_path)
                print(f"Archivo: {file_path}, Métodos en Clases: {methods_count}, Métodos en Interfaces: {interface_methods_count}")
                total_methods += methods_count
                total_interface_methods += interface_methods_count

    return total_methods, total_interface_methods

# Contar los métodos en el directorio raíz y todos los subdirectorios
total_methods_count, total_interface_methods_count = count_methods_recursively(ROOT_DIR)
print(f"Total de métodos en clases encontrados: {total_methods_count}")
print(f"Total de métodos en interfaces encontrados: {total_interface_methods_count}")
