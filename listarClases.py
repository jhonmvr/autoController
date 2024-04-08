import os
import javalang
OUTPUT_FILE = './listarClasesObject.txt'

def load_processed_imports(output_file):
    processed_imports = {}
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('import'):
                    full_class_path = line.split(' ')[1].rstrip(';\n')
                    class_name = full_class_path.split('.')[-1]
                    processed_imports[class_name] = full_class_path
    return processed_imports
listaReturns = ['List<Object>','Object','List<?>','Map<String, Object>','List<Object[]>','Object[]','List<>','Class','Class<>']
processed_imports = load_processed_imports(OUTPUT_FILE)
imports_set = set()
def format_type(node):

    if isinstance(node, javalang.tree.ReferenceType):
        if node.arguments:
            args = [format_type(arg.type) for arg in node.arguments if arg.type is not None]
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
            param_type = param.type
            # Verificar si el tipo es simple o complejo
            params_all.append((param_type, param.name, ""))

            annotation = f'@RequestParam("{param.name}")'
            params.append(format_type(param_type))

            # Manejar parámetros complejos
            complex_params.append((param_type, param.name))
        mapper_service = node.return_type
        mapper_name = None

        if mapper_service:
            mapper_name = mapper_service
            mappers.add((mapper_service, mapper_name))

        methods_info.append((method_name,return_type, params))


    return package_name, methods_info, mappers
def is_not_interface(java_file_path):
    with open(java_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    tree = javalang.parse.parse(content)

    # Buscar nodos de tipo InterfaceDeclaration en el árbol
    for _, node in tree.filter(javalang.tree.InterfaceDeclaration):
        return False  # Si encuentra una declaración de interfaz, retorna False

    return True  # Si no encuentra ninguna declaración de interfaz, retorna True

def extract_classes_and_generate_imports(project_dir, output_file):


    for root, dirs, files in os.walk(project_dir):
        for file in files:
            print("file",file)
            if file.endswith('.java'):
                path = os.path.join(root, file)
                service_path = os.path.join(root, path)
                if(is_not_interface(service_path)):
                    print(f" {service_path}, No es una interface omitiendo...")
                    continue
            # Extraer nombres de métodos dinámicamente

            package_name, methods, mappers = get_service_methods(service_path)

            if not methods:  # Si no hay métodos, continúa con el siguiente archivo
                print(f"No se encontraron métodos en {path}, omitiendo...")
                continue


            class_name = file[:-5]
            for method_name,return_type, params in  methods:
                try:

                    if class_name in processed_imports:
                        continue
                    print("params>>>>>>>>>",params)
                    if return_type in listaReturns or any(elemento in params for elemento in listaReturns):
                        import_line = f"import {package_name}.{class_name};"
                        imports_set.add(import_line)

                except javalang.parser.JavaSyntaxError as e:
                    print(f"Syntax error in {path}: {e}")

    with open(output_file, 'a', encoding='utf-8') as f:
        for import_line in sorted(imports_set):
            f.write(import_line + '\n')

# Asegúrate de ajustar las rutas según tu entorno

project_dir = 'C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp\\negocio\\gestor'
output_file = 'listarClasesObject.txt'
extract_classes_and_generate_imports(project_dir, output_file)

print("import añadidos",len(imports_set))
