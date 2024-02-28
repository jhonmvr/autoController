import os
import sys
import inspect
from jinja2 import Environment, FileSystemLoader
import javalang
from collections import defaultdict
# Asegúrate de que Python pueda encontrar tus módulos de servicio
#sys.path.append('C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\gestor\\web')

# Configuración
SERVICE_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\gestor'

# Paso 1: Extraer la base del directorio y las partes específicas
base_dir = SERVICE_DIR.split('erp-negocio')[0]  # Obtiene la base hasta 'erp-negocio'
specific_part = SERVICE_DIR.split('erp-negocio\\src\\main\\java\\')[1]  # Obtiene la parte específica después de 'java\\'

# Paso 2: Reemplazar 'negocio' por 'controller' en la parte específica
specific_part = specific_part.replace('negocio', 'controller')

# Paso 3: Construir el nuevo directorio para CONTROLLER_DIR
CONTROLLER_DIR = os.path.join(base_dir, 'erp-rest\\src\\main\\java', specific_part)
#CONTROLLER_DIR = "./repuest"
print(CONTROLLER_DIR)


TEMPLATE_FILE = 'controller_template.txt'  # Nombre del archivo de plantilla
sys.path.append(SERVICE_DIR)
# Cargar plantilla
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template(TEMPLATE_FILE)

def format_type(node):
    """Formatea el tipo de nodo de javalang a una cadena adecuada para Java, incluidos los tipos genéricos."""
    if isinstance(node, javalang.tree.ReferenceType):
        if node.arguments:
            # Manejar tipos genéricos, ej. List<Long>
            args = [format_type(arg.type) for arg in node.arguments if arg.type is not None]
            generic_args = ", ".join(args)
            return f"{node.name}<{generic_args}>"
        return node.name
    elif isinstance(node, javalang.tree.BasicType):
        # Tipos básicos como int, long, etc.
        return node.name
    elif node is None:
        return None  # Caso para tipos void
    else:
        # Por defecto, convertir el nodo a cadena (para manejar otros casos potenciales)
        return str(node)


def get_service_methods(service_path):
    """Extrae los nombres de los métodos, sus tipos de retorno, y parámetros de un archivo de servicio Java."""
    methods_info = []
    package_name = None

    with open(service_path, 'r', encoding='utf-8') as file:
        content = file.read()

    tree = javalang.parse.parse(content)

    if tree.package:
        package_name = tree.package.name

    # Definir tipos considerados como 'simples' o primitivos para @RequestParam
    simple_types = {"String", "int", "long", "double", "float", "boolean", "Integer", "Long", "Double", "Float", "Boolean", "char", "Character"}

    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        return_type = format_type(node.return_type)
        params = []
        for param in node.parameters:
            param_type = format_type(param.type)
            # Si es un tipo simple, usamos @RequestParam con el nombre del parámetro
            if param.type.name in simple_types:
                annotation = f'@RequestParam("{param.name}")'
            else:
                annotation = "@RequestBody"
            params.append((param_type, param.name, annotation))
        http_method = "Post" if any(p[2] == "@RequestBody" for p in params) else "Get"
        methods_info.append((node.name, return_type, params, http_method))

    return package_name, methods_info

def adjust_method_paths(methods_info):
    """
    Ajusta las rutas de los métodos para asegurar que sean únicas dentro del controlador.
    Añade /v1, /v2, etc., a las rutas duplicadas.
    """
    path_counts = defaultdict(int)
    adjusted_methods = []

    for method, return_type, params, http_method in methods_info:
        # Generar la ruta base del método (puede ser simplemente el nombre del método)
        base_path = method.lower()
        path_counts[base_path] += 1

        # Comprobar si la ruta ya fue utilizada
        if path_counts[base_path] > 1:
            # Añadir el sufijo de versión si la ruta está duplicada
            versioned_path = f"{base_path}/v{path_counts[base_path]}"
        else:
            versioned_path = base_path

        # Añadir la información del método ajustado a la lista
        adjusted_methods.append((method, return_type, params, http_method, versioned_path))

    return adjusted_methods

def is_not_interface(java_file_path):
    with open(java_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    tree = javalang.parse.parse(content)

    # Buscar nodos de tipo InterfaceDeclaration en el árbol
    for _, node in tree.filter(javalang.tree.InterfaceDeclaration):
        return False  # Si encuentra una declaración de interfaz, retorna False

    return True  # Si no encuentra ninguna declaración de interfaz, retorna True

# Procesar cada archivo de servicio
for root, dirs, files in os.walk(SERVICE_DIR):
    for service_file in files:

        if service_file.endswith('.java'):

            service_path = os.path.join(root, service_file)
            if(is_not_interface(service_path)):
                print(f" {service_file}, No es una interface omitiendo...")
                continue
            # Extraer nombres de métodos dinámicamente
            package_name, methods = get_service_methods(service_path)

            if not methods:  # Si no hay métodos, continúa con el siguiente archivo
                print(f"No se encontraron métodos en {service_file}, omitiendo...")
                continue

            # A continuación, calculamos CONTROLLER_DIR basado en package_name
            package_path = package_name.replace('.', '\\')  # Convertir el nombre del paquete a ruta de directorio
            dynamic_controller_dir = os.path.join(base_dir, 'erp-rest\\src\\main\\java', package_path.replace('negocio', 'controller'))

            if not os.path.exists(dynamic_controller_dir):
                os.makedirs(dynamic_controller_dir)


            controller_package = package_name.replace('negocio', 'controller')
            service_name = service_file[:-5]  # Sin '.py'
            controller_name = 'C' + service_name[1:]  # 'N' por 'C'
            request_mapping = controller_package.replace('.', '/').lower() + '/' + controller_name
            request_mapping = request_mapping.split('controller')[1]
            adjusted_methods = adjust_method_paths(methods)
            # Renderizar plantilla
            controller_content = template.render(
                package=controller_package,
                controller_name=controller_name,
                service_name=service_name,
                request_mapping=request_mapping,
                methods=adjusted_methods
            )

            # Guardar archivo de controlador generado en la ruta dinámica
            with open(os.path.join(dynamic_controller_dir, controller_name + '.java'), 'w') as f:
                f.write(controller_content)
            print(f'Controlador generado: {controller_name}.java en {dynamic_controller_dir}')
