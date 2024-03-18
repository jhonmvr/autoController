import os
import sys
import inspect
from jinja2 import Environment, FileSystemLoader
import javalang
from collections import defaultdict
# Asegúrate de que Python pueda encontrar tus módulos de servicio
#sys.path.append('C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\gestor\\web')

# Configuración
SERVICE_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\servicios'
#SERVICE_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\servicios\\bdg'
#C:\WORKSPACE\SUKASA\erp\erp-rest\src\main\java\com\erp\controller\gestor\bdg
# Paso 1: Extraer la base del directorio y las partes específicas
base_dir = SERVICE_DIR.split('erp-negocio')[0]  # Obtiene la base hasta 'erp-negocio'
specific_part = SERVICE_DIR.split('erp-negocio\\src\\main\\java\\')[1]  # Obtiene la parte específica después de 'java\\'

# Paso 2: Reemplazar 'negocio' por 'controller' en la parte específica
specific_part = specific_part.replace('negocio', 'controller')

# Paso 3: Construir el nuevo directorio para CONTROLLER_DIR
CONTROLLER_DIR = os.path.join(base_dir, 'erp-rest\\src\\main\\java', specific_part)
FILE_IMPORTS = './imports.txt'
FILE_TABLAS_VACIAS = './tablas_vacias.txt'
#CONTROLLER_DIR = "./repuest"
print(CONTROLLER_DIR)


TEMPLATE_FILE = 'controller_template.txt'  # Nombre del archivo de plantilla
sys.path.append(SERVICE_DIR)
# Cargar plantilla
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template(TEMPLATE_FILE)

#METODO QUE LEE TODOS LOS IMPORTS DEL ARCHIVO PLANO
def read_all_imports():
    """Lee todos los imports desde el archivo generado y los devuelve como un diccionario."""
    imports_dict = {}
    with open(FILE_IMPORTS, 'r') as f:
        for line in f:
            # Asume que el archivo tiene líneas que comienzan con 'import ' seguido por el tipo completo
            if line.startswith('import ') and 'tablas' in line and not 'enumeradores' in line:
                full_type = line.strip().split(' ')[1].rstrip(';')
                simple_type = full_type.split('.')[-1]
                if not simple_type.startswith('Enum'):
                    imports_dict[simple_type] = full_type
    return imports_dict

all_imports = read_all_imports()

#METODO QUE LEE TODOS LOS IMPORTS DEL ARCHIVO PLANO
def read_all_tablas_vacias():
    """Lee todos los imports desde el archivo generado y los devuelve como un diccionario."""
    imports_dict = {}
    with open(FILE_TABLAS_VACIAS, 'r') as f:
        for line in f:
            # Asume que el archivo tiene líneas que comienzan con 'import ' seguido por el tipo completo
            imports_dict[line.strip()] = line.strip()
    return imports_dict

tablas_vacias = read_all_tablas_vacias()
#print("tablas******************************",tablas_vacias)

def read_all_Enum_in_imports():
    """Lee todos los imports desde el archivo generado y los devuelve como un diccionario."""
    imports_dict = {
    "String",
    "int", "long", "double", "float", "boolean", "char",
    "Integer", "Long", "Double", "Float", "Boolean", "Character",
    "byte", "short",
    "Byte", "Short"
    }

    with open(FILE_IMPORTS, 'r') as f:
        for line in f:
            # Asume que el archivo tiene líneas que comienzan con 'import ' seguido por el tipo completo
            if line.startswith('import '):
                full_type = line.strip().split(' ')[1].rstrip(';')
                simple_type = full_type.split('.')[-1]
                if simple_type.startswith('Enum'):
                    imports_dict.add(simple_type)
    return imports_dict
simple_types = read_all_Enum_in_imports()
#print("simple_types>>>>>>>>>>>>>>>>>>>>>>>>>>",simple_types)
# Al inicio del script, después de definir las constantes

#print("allimports",all_imports)
def agregar_dto(arg):
    if arg in all_imports:
      return arg + 'Dto'
    return arg

#validar si no se debe mappear entidades de tablas vacias
def validar_tablas_vacias(node):
    if node in tablas_vacias:
        return True
    return False

def format_type(node):

    if isinstance(node, javalang.tree.ReferenceType):
        if node.arguments:
            args = [format_type(arg.type) for arg in node.arguments if arg.type is not None]
            generic_args = ", ".join(args)
            if validar_tablas_vacias(generic_args):
                return f"{node.name}<{generic_args}>"
            return f"{node.name}<{agregar_dto(generic_args)}>"
        if node.dimensions:
            # Handle arrays, even when ArrayType is not a separate class
            if validar_tablas_vacias(node.name):
                return f"{node.name}{'[]' * len(node.dimensions)}"
            return f"{agregar_dto(node.name)}{'[]' * len(node.dimensions)}"
        if validar_tablas_vacias(node.name):
            return node.name
        return agregar_dto(node.name)
    elif isinstance(node, javalang.tree.BasicType):
        return node.name
    elif node is None:
        return 'void'
    else:
        return str(node)

def agregar_mapper(arg):

    return arg + 'Mapper'


def format_type_to_mapper(node):
    mappper = ""
    #print("node************",node)
    if isinstance(node, javalang.tree.ReferenceType):
        if node.arguments:
            args = [format_type_param(arg.type) for arg in node.arguments if arg.type is not None]
            generic_args = ", ".join(args)
            mappper = generic_args
        else:
            mappper = node.name
    else:
        mappper = str(node)

    if mappper in all_imports and not mappper in tablas_vacias:
        #print("mappper************",mappper)
        return mappper + 'Mapper'
    return None


def format_type_to_mapper_toDto(node):
    mappper = ""

    if isinstance(node, javalang.tree.ReferenceType):
        if node.arguments:
            args = [format_type_param(arg.type) for arg in node.arguments if arg.type is not None]
            generic_args = ", ".join(args)

            if generic_args in all_imports:
                return 'toDtoList'

        mappper = node.name
    else:
        mappper = str(node)

    if mappper in all_imports:
      return 'toDto'
    return None


def format_type_param(node):
    if isinstance(node, javalang.tree.ReferenceType):
        if node.arguments:
            args = [format_type_param(arg.type) for arg in node.arguments if arg.type is not None]
            generic_args = ", ".join(args)
            return f"{node.name}<{generic_args}>"
        if node.dimensions:
            # Handle arrays, even when ArrayType is not a separate class
            return f"{node.name}{'[]' * len(node.dimensions)}"
        return node.name
    elif isinstance(node, javalang.tree.BasicType):
        return node.name
    elif node is None:
        return 'void'
    else:
        return str(node)




def get_service_methods(service_path):
    methods_info = []
    package_name = None
    mappers = set()

    with open(service_path, 'r', encoding='utf-8') as file:
        content = file.read()

    tree = javalang.parse.parse(content)

    if tree.package:
        package_name = tree.package.name


    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        return_type = format_type(node.return_type)
        excepciones = []
        method_name = node.name
        if node.throws:

            for tr in node.throws:
                excepciones = tr

        params = []
        complex_params = []
        params_all = []
        for param in node.parameters:
            param_type = format_type_param(param.type)
            # Verificar si el tipo es simple o complejo
            params_all.append((param_type, param.name, ""))
            if param.type.name in simple_types:
                annotation = f'@RequestParam("{param.name}")'
                params.append((param_type, param.name, annotation))
            else:
                # Manejar parámetros complejos
                complex_params.append((param_type, param.name))

        # Si hay más de un parámetro complejo, encapsularlos en un mapa de parámetros
        if len(complex_params) > 1:
            # Asumiendo que quieres usar un DTO para esto, lo marcamos como tal.
            # Deberías crear un DTO que encapsule estos parámetros en tu código Java.
            annotation = "@RequestBody"
            params.append(("Map<String, Object>", "body", annotation))
            http_method = "Post"
        elif len(complex_params) == 1:
            # Solo un parámetro complejo, se maneja normalmente
            param_type, param_name = complex_params[0]
            annotation = "@RequestBody"
            params.append((param_type, param_name, annotation))
            http_method = "Post"
        else:
            # No hay parámetros complejos o solo uno, determinar el método HTTP basado en los parámetros existentes
            http_method = "Get" if all(param[2] == '@RequestParam' for param in params) else "Post"


        mapper_service = format_type_to_mapper(node.return_type)
        mapper_name = None

        if mapper_service:
            mapper_name = mapper_service[0].lower() + mapper_service[1:]
            mappers.add((mapper_service, mapper_name))

        methods_info.append((method_name, node.name, return_type, params, http_method,complex_params,params_all,(mapper_name,format_type_to_mapper_toDto(node.return_type)), excepciones))


    return package_name, validar_metodos_duplicados(methods_info), mappers

def validar_metodos_duplicados(methods_info):
    ###inicio
    vistos = set()

    # Lista para almacenar los métodos sin duplicados
    methods_info_sin_duplicados = []

    for method_info in methods_info:
        metodo_name, node_name, return_type, params, http_method, complex_params, params_all, (map_name, format_mapper), excepciones = method_info

        # Crear una tupla con las características relevantes
        caracteristicas = (return_type, tuple(params), node_name)

        # Verificar si ya hemos visto estas características antes
        if caracteristicas not in vistos:
            # Agregar las características al conjunto de métodos vistos
            vistos.add(caracteristicas)

            # Agregar el método a la lista sin duplicados
            methods_info_sin_duplicados.append(method_info)
    ##fin
    return methods_info_sin_duplicados

def cambiar_nombre_metodo_ya_definido(methods_info):

    vistos = set()
    for method_info in methods_info:
        method_name, node_name, return_type, params, http_method, complex_params, params_all, (map_name, format_mapper), excepciones = method_info
        caracteristicas = (tuple(params), node_name)
        if caracteristicas in vistos:
            vistos.add(caracteristicas)
            return True
    return False

def adjust_method_paths(methods_info):
    """
    Ajusta las rutas de los métodos para asegurar que sean únicas dentro del controlador.
    Añade /v1, /v2, etc., a las rutas duplicadas.
    """
    path_counts = defaultdict(int)
    adjusted_methods = []

    for method_name, method, return_type, params, http_method, complex_params, params_all, toDto, excepciones in methods_info:
        # Generar la ruta base del método (puede ser simplemente el nombre del método)
        base_path = method
        path_counts[base_path] += 1

        # Comprobar si la ruta ya fue utilizada
        if path_counts[base_path] > 1:
            # Añadir el sufijo de versión si la ruta está duplicada
            versioned_path = f"{base_path}/v{path_counts[base_path]}"
            if cambiar_nombre_metodo_ya_definido(methods_info):
                method_name = f"{method_name}V{path_counts[base_path]}"
        else:
            versioned_path = base_path

        # Añadir la información del método ajustado a la lista
        adjusted_methods.append((method_name, method, return_type, params, http_method,complex_params, params_all, versioned_path,toDto,excepciones))

    return adjusted_methods

def is_not_interface(java_file_path):
    with open(java_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    tree = javalang.parse.parse(content)

    # Buscar nodos de tipo InterfaceDeclaration en el árbol
    for _, node in tree.filter(javalang.tree.InterfaceDeclaration):
        return False  # Si encuentra una declaración de interfaz, retorna False

    return True  # Si no encuentra ninguna declaración de interfaz, retorna True

# Procesar cada archivo de servicio y crear los controladores en sus respectiva carpeta
for root, dirs, files in os.walk(SERVICE_DIR):
    for service_file in files:

        if service_file.endswith('.java'):

            service_path = os.path.join(root, service_file)
            if(is_not_interface(service_path)):
                print(f" {service_file}, No es una interface omitiendo...")
                continue
            # Extraer nombres de métodos dinámicamente

            package_name, methods, mappers = get_service_methods(service_path)

            if not methods:  # Si no hay métodos, continúa con el siguiente archivo
                print(f"No se encontraron métodos en {service_file}, omitiendo...")
                continue

            # A continuación, calculamos CONTROLLER_DIR basado en package_name
            package_path = package_name.replace('.', '\\')  # Convertir el nombre del paquete a ruta de directorio
            dynamic_controller_dir = os.path.join(base_dir, 'erp-rest\\src\\main\\java', package_path.replace('negocio', 'controller'))

            if not os.path.exists(dynamic_controller_dir):
                os.makedirs(dynamic_controller_dir)


            controller_package = package_name.replace('negocio', 'controller')
            service_name = service_file[:-5]  # Sin '.java'
            # 'N' por 'C' Servicio
            if service_name.startswith('Servicio'):
                controller_name = 'C' + service_name
            if service_name.startswith('N'):
                controller_name = 'C' + service_name[1:]


            request_mapping = controller_package.replace('.', '/').lower() + '/' + controller_name
            request_mapping = request_mapping.split('controller')[1]
            adjusted_methods = adjust_method_paths(methods)
            # Renderizar plantilla
            controller_content = template.render(
                package=controller_package,
                controller_name=controller_name,
                service_name=service_name,
                request_mapping=request_mapping,
                methods=adjusted_methods,
                mappers= mappers
            )

            # Guardar archivo de controlador generado en la ruta dinámica
            with open(os.path.join(dynamic_controller_dir, controller_name + '.java'), 'w') as f:
                f.write(controller_content)
            print(f'Controlador generado: {controller_name}.java en {dynamic_controller_dir}')


