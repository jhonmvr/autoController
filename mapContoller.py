import os
import sys
import inspect
from jinja2 import Environment, FileSystemLoader
import javalang
# Asegúrate de que Python pueda encontrar tus módulos de servicio
#sys.path.append('C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\gestor\\web')

# Configuración
SERVICE_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\gestor\\inv'

# Paso 1: Extraer la base del directorio y las partes específicas
base_dir = SERVICE_DIR.split('erp-negocio')[0]  # Obtiene la base hasta 'erp-negocio'
specific_part = SERVICE_DIR.split('erp-negocio\\src\\main\\java\\')[1]  # Obtiene la parte específica después de 'java\\'

# Paso 2: Reemplazar 'negocio' por 'controller' en la parte específica
specific_part = specific_part.replace('negocio', 'controller')

# Paso 3: Construir el nuevo directorio para CONTROLLER_DIR
CONTROLLER_DIR = os.path.join(base_dir, 'erp-rest\\src\\main\\java', specific_part)

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




# Procesar cada archivo de servicio
for service_file in os.listdir(SERVICE_DIR):
    service_path = os.path.join(SERVICE_DIR, service_file)
    if os.path.isfile(service_path) and service_file.endswith('.java'):
        # Extraer nombres de métodos dinámicamente
        package_name, methods = get_service_methods(service_path)

        if not methods:  # Si no hay métodos, continúa con el siguiente archivo
            print(f"No se encontraron métodos en {service_file}, omitiendo...")
            continue

        controller_package = package_name.replace('negocio', 'controller')
        service_name = service_file[:-5]  # Sin '.py'
        controller_name = 'C' + service_name[1:]  # 'N' por 'C'
        request_mapping = controller_package.replace('.', '/').lower() + '/' + controller_name
        request_mapping = request_mapping.split('controller')[1]
        # Renderizar plantilla
        controller_content = template.render(
            package=controller_package,
            controller_name=controller_name,
            service_name=service_name,
            request_mapping=request_mapping,
            methods=methods
        )
        if not os.path.exists(CONTROLLER_DIR):
            os.makedirs(CONTROLLER_DIR)
        # Guardar archivo de controlador generado
        with open(os.path.join(CONTROLLER_DIR, controller_name + '.java'), 'w') as f:
            f.write(controller_content)
        print(f'Controlador generado: {controller_name}.java')
