import os
import re

# Rutas de los directorios donde buscar las clases
PROJECT_DIRS = [
    'C:\\WORKSPACE\\SUKASA\\erp\\erp-negocio\\src\\main\\java\\com\\erp',
    'C:\\WORKSPACE\\SUKASA\\erp\\erp-modelo\\src\\main\\java\\com\\erp'
]

# Archivo de entrada y salida
INPUT_FILE = './import_imcompleto.txt'
OUTPUT_FILE = './completed_imports.txt'

def find_class_package_or_import(class_name):
    """Primero busca la declaración de paquete en el archivo de la clase. Si no se encuentra, busca en declaraciones de import."""
    # Intentar encontrar la declaración de paquete directamente
    package_regex = re.compile(r'^package\s+(.*);')
    import_regex = re.compile(fr'import\s+(.*\b{class_name});')

    for project_dir in PROJECT_DIRS:
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if file[:-5] == class_name:  # Si el nombre del archivo coincide con la clase
                            for line in f:
                                pkg_match = package_regex.match(line)
                                if pkg_match:
                                    return f"import {pkg_match.group(1)}.{class_name};"
                        else:  # Buscar en declaraciones de import
                            for line in f:
                                import_match = import_regex.match(line)
                                if import_match:
                                    return import_match.group(0) + ";"

    return None  # Retorna None si no se encuentra la clase

def process_imports(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            class_name_search = re.search(r'import\s+(\w+);', line)
            if class_name_search:
                class_name = class_name_search.group(1)
                full_import = find_class_package_or_import(class_name)
                if full_import:
                    outfile.write(full_import + '\n')
                else:
                    print(f"No se encontró la declaración de import para: {class_name}")
            else:
                outfile.write(line)  # Escribir la línea tal cual si no coincide con el patrón

# Ejecutar el procesamiento
process_imports(INPUT_FILE, OUTPUT_FILE)

print(f"Los imports completos han sido escritos en: {OUTPUT_FILE}")
