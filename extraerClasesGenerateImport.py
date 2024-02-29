import os
import javalang
OUTPUT_FILE = './imports.txt'

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

processed_imports = load_processed_imports(OUTPUT_FILE)
imports_set = set()
def extract_classes_and_generate_imports(project_dir, output_file):


    for root, dirs, files in os.walk(project_dir):
        for file in files:
            print("file",file)
            if file.endswith('.java'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                try:
                    tree = javalang.parse.parse(content)
                    if tree.package:
                        package_name = tree.package.name
                        for type_decl in tree.types:
                            class_name = type_decl.name
                            if class_name in processed_imports:
                                continue
                            import_line = f"import {package_name}.{class_name};"

                            imports_set.add(import_line)
                except javalang.parser.JavaSyntaxError as e:
                    print(f"Syntax error in {path}: {e}")

    with open(output_file, 'a', encoding='utf-8') as f:
        for import_line in sorted(imports_set):
            f.write(import_line + '\n')

# Asegúrate de ajustar las rutas según tu entorno

project_dir = 'C:\\WORKSPACE\\SUKASA\\erp\\'
output_file = 'imports.txt'
extract_classes_and_generate_imports(project_dir, output_file)

print("import añadidos",len(imports_set))
