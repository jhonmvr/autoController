import os
import sys
import inspect
from jinja2 import Environment, FileSystemLoader
import javalang
# Asegúrate de que Python pueda encontrar tus módulos de servicio
#sys.path.append('C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\gestor\\web')

# Configuración
SERVICE_DIR = 'C:\\WORKSPACE\\erp-rest\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\gestor\\bdg'  # Ruta al directorio de interfaces de servicio
#CONTROLLER_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-rest\\src\\main\\java\\com\\erp\\controller\\gestor\\web'  # Ruta al directorio donde se guardarán los controladores generados
CONTROLLER_DIR = './respuest'  # Ruta al directorio donde se guardarán los controladores generados
TEMPLATE_FILE = 'controller_template.txt'  # Nombre del archivo de plantilla
sys.path.append(SERVICE_DIR)
# Cargar plantilla
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template(TEMPLATE_FILE)

def get_service_methods(service_path):
    """Extrae los nombres de los métodos y sus tipos de retorno de un archivo de servicio Java."""
    methods_info = []
    package_name = None

    with open(service_path, 'r', encoding='utf-8') as file:
        content = file.read()

    tree = javalang.parse.parse(content)

    if tree.package:
        package_name = tree.package.name

    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        # Añadir tanto el nombre del método como su tipo de retorno
        methods_info.append((node.name, node.return_type))

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
        request_mapping = service_name[1:].lower()

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

