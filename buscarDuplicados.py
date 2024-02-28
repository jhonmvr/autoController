import os
import javalang

# Define el directorio donde se encuentran tus archivos de controlador
CONTROLLER_DIR = 'C:\\WORKSPACE\\erp-rest\\erp-rest\\src\\main\\java\\com\\erp'

def analyze_java_files(directory):
    method_signatures = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as java_file:
                    content = java_file.read()

                try:
                    tree = javalang.parse.parse(content)
                    for _, class_node in tree.filter(javalang.tree.ClassDeclaration):
                        for _, method_node in class_node.filter(javalang.tree.MethodDeclaration):
                            method_signature = f"{method_node.name}({', '.join(param.type.name for param in method_node.parameters)})"
                            class_method_signature = f"{class_node.name}.{method_signature}"

                            if method_node.name not in method_signatures:
                                method_signatures[method_node.name] = [class_method_signature]
                            else:
                                method_signatures[method_node.name].append(class_method_signature)
                except javalang.parser.JavaSyntaxError as e:
                    print(f"Syntax error processing file {file_path}: {e}")

    return method_signatures

def find_duplicate_methods(method_signatures):
    duplicates = {method: signatures for method, signatures in method_signatures.items() if len(signatures) > 1}
    return duplicates

def print_duplicate_methods(duplicates):
    if duplicates:
        
        for method, signatures in duplicates.items():
            print(f"\nMethod: {method}")
            for signature in signatures:
                print(f"  - {signature}")
                
        print("Found methods with the same name but different signatures:",len(duplicates))
    else:
        print("No duplicate method names with different signatures found.")

if __name__ == "__main__":
    method_signatures = analyze_java_files(CONTROLLER_DIR)
    duplicates = find_duplicate_methods(method_signatures)
    print_duplicate_methods(duplicates)
