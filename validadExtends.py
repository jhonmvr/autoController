import javalang

def extract_generic_info(java_source):
    tree = javalang.parse.parse(java_source)
    base_class_name = None
    generic_type_name = None
    for _, class_decl in tree.filter(javalang.tree.InterfaceDeclaration):
        if class_decl.extends:
            base_reference_type = class_decl.extends[0]
            base_class_name = base_reference_type.name
            if base_reference_type.arguments:
                first_argument = base_reference_type.arguments[0]
                if isinstance(first_argument.type, javalang.tree.ReferenceType):
                    generic_type_name = first_argument.type.name

    return base_class_name, generic_type_name

# Uso de la función
java_source = """
public interface NAchiqueDestino extends GenericoServicio<BdgDtAchiqueDestino> {

List<VwZonasAchique> zonasAchiqueDestino(Long idAchique);

List<VwZonasAchique> zonasAchiqueDestinoProcesar(Long idAchique);


}
"""

base_class, generic_type = extract_generic_info(java_source)

if base_class and generic_type:
    print(f"Clase base: {base_class}")
    print(f"Tipo de parámetro genérico: {generic_type}")
else:
    print("La clase no extiende GenericoServicio con un parámetro genérico específico.")
