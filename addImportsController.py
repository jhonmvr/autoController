import os
import sys
import inspect
from jinja2 import Environment, FileSystemLoader
import javalang
from collections import defaultdict
CONTROLLER_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-rest\\src\\main\\java\\com\\erp\\controller\\servicios'
#CONTROLLER_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-web\\src\\main\\java\\com\\erp\\cliente\\rest\\servicios'
#com.erp.controller.gestor.bdg;
FILE_IMPORTS = './imports.txt'
#METODO QUE LEE TODOS LOS IMPORTS DEL ARCHIVO PLANO
def read_all_imports():
    """Lee todos los imports desde el archivo generado y los devuelve como un diccionario."""
    imports_dict = {}
    with open(FILE_IMPORTS, 'r') as f:
        for line in f:
            # Asume que el archivo tiene líneas que comienzan con 'import ' seguido por el tipo completo
            if line.startswith('import '):
                full_type = line.strip().split(' ')[1].rstrip(';')
                #print("full_type=============",full_type)
                simple_type = full_type.split('.')[-1]
                #print("simple_type=============",simple_type)
                imports_dict[simple_type] = full_type
    return imports_dict

# Al inicio del script, después de definir las constantes
all_imports = read_all_imports()

#metodos para añadir los imports
def find_data_types_in_controller(controller_path):
    """Encuentra los tipos de datos utilizados en un controlador."""
    data_types = set()
    try:
        with open(controller_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(controller_path, 'r', encoding='ISO-8859-1') as file:
            content = file.read()

    tokens = list(javalang.tokenizer.tokenize(content))

    for token in tokens:
        if isinstance(token, javalang.tokenizer.Identifier):
            data_types.add(token.value)
    return data_types


def add_imports_to_controller(controller_path, all_imports):

    """Añade imports necesarios a un archivo de controlador."""
    data_types = find_data_types_in_controller(controller_path)

    necessary_imports = set()
    for data_type in data_types:
        #print("data_type===========>",data_type)
        if data_type in all_imports:
            #print("tokens===========>",data_type)
            necessary_imports.add(all_imports[data_type])

    # Leer el contenido original del controlador
    try:
        with open(controller_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
    except UnicodeDecodeError:
        with open(controller_path, 'r', encoding='ISO-8859-1') as file:
            original_content = file.read()

    # Preparar el nuevo contenido con los imports añadidos
    # Suponiendo que original_content ya contiene el contenido del archivo leído
    first_line, rest_of_content = original_content.split('\n', 1)
    imports_content = '\n'.join(sorted(f'import {imp};' for imp in necessary_imports))

    # Combinar la primera línea (declaración del paquete), los imports y el resto del contenido
    new_content = f"{first_line}\n{imports_content}\n\n{rest_of_content}"


    # Sobrescribir el controlador con el nuevo contenido
    with open(controller_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

print("*****************IMPORTS********************************")
for root, dirs, files in os.walk(CONTROLLER_DIR):
    for file in files:
        if file.endswith('.java'):
            controller_path = os.path.join(root, file)
            print(f'CONTROLADOR {controller_path}')
            add_imports_to_controller(controller_path, all_imports)
