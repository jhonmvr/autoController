import os
import javalang

SERVICE_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio'
MODEL_DIR = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-modelo\\src\\main\\java\\com\\erp'
OUTPUT_FILE = './correct_package_non_primitive_types.txt'

JAVA_PRIMITIVE_TYPES = {"byte", "short", "int", "long", "float", "double", "boolean", "char"}
JAVA_OWN_TYPES = {"String", "Long", "Integer", "Double", "Float", "Boolean", "Character", "Number", "Object", "Short", "T"}

package_cache = {}

def is_excluded_type(type_name):
    return type_name in JAVA_PRIMITIVE_TYPES or type_name in JAVA_OWN_TYPES

def find_class_package(class_name):
    if class_name in package_cache:
        return package_cache[class_name]

    for root, _, files in os.walk(MODEL_DIR):
        for file in files:
            if file.endswith('.java') and file[:-5] == class_name:
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('package'):
                            package_name = line.split()[1].rstrip(';')
                            full_class_name = f"{package_name}.{class_name}"
                            package_cache[class_name] = full_class_name
                            return full_class_name
    return None

def process_type(type_name, non_primitive_types_with_correct_package):
    if not is_excluded_type(type_name):
        package = find_class_package(type_name)
        if package:
            non_primitive_types_with_correct_package.add(package)

def get_non_primitive_types_with_correct_package(service_path):
    non_primitive_types_with_correct_package = set()

    with open(service_path, 'r', encoding='utf-8') as file:
        content = file.read()

    tree = javalang.parse.parse(content)

    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        if node.return_type and not is_excluded_type(node.return_type.name):
            process_type(node.return_type.name, non_primitive_types_with_correct_package)

        for param in node.parameters:
            if not is_excluded_type(param.type.name):
                process_type(param.type.name, non_primitive_types_with_correct_package)

    return non_primitive_types_with_correct_package

all_types_with_correct_package = set()
for root, dirs, files in os.walk(SERVICE_DIR):
    for file in files:
        if file.endswith('.java'):
            types_with_correct_package = get_non_primitive_types_with_correct_package(os.path.join(root, file))
            all_types_with_correct_package.update(types_with_correct_package)

if not os.path.exists(os.path.dirname(OUTPUT_FILE)):
    os.makedirs(os.path.dirname(OUTPUT_FILE))
with open(OUTPUT_FILE, 'w') as f:
    for full_class_name in sorted(all_types_with_correct_package):
        f.write(f'import {full_class_name};\n')

print(f'Total de tipos de datos no primitivos únicos guardados (incluyendo el paquete correcto): {len(all_types_with_correct_package)}')
print(f'Archivo generado con tipos de datos no primitivos y específicos de la aplicación (incluyendo el paquete correcto): {OUTPUT_FILE}')
