def generate_service_classes(db_structure, output_dir, table_index, package_name):
    try:
        table_name = list(db_structure.keys())[table_index]
        class_name = pascal_case(table_name)

        # Create service directories
        service_dir = os.path.join(output_dir, 'service')
        service_impl_dir = os.path.join(service_dir, 'impl')
        os.makedirs(service_dir, exist_ok=True)
        os.makedirs(service_impl_dir, exist_ok=True)
        print(f"Service directories created: {service_dir}, {service_impl_dir}")

        # Generate Service Interface
        service_interface_path = os.path.join(service_dir, f"{class_name}Service.java")
        with open(service_interface_path, 'w') as f:
            f.write(f"package {package_name}.service;\n\n")
            f.write(f"import {package_name}.dto.{class_name}DTO; \n\n")
            f.write(f"import java.util.List;\n\n")
            f.write(f"public interface {class_name}Service {{\n")
            f.write(f"List<{class_name}DTO> findAll();\n")
            f.write(f"List<{class_name}DTO> findById(Long id);\n")
            f.write(f"{class_name}DTO update(Long id, {class_name}DTO dto);\n")  # Added update method
            f.write("}\n")

        print(f"Service interface {class_name}Service.java generated successfully.")

        # Generate Service Implementation
        service_impl_path = os.path.join(service_impl_dir, f"{class_name}ServiceImpl.java")
        with open(service_impl_path, 'w') as f:
            f.write(f"package {package_name}.service.impl;\n\n")

            f.write(f"import {package_name}.dto.{class_name}DTO;\n")
            f.write(f"import {package_name}.entity.{class_name};\n")
            f.write(f"import {package_name}.repository.{class_name}Repository;\n")
            f.write(f"import {package_name}.service.{class_name}Service;\n\n")

            f.write("import org.springframework.beans.factory.annotation.Autowired;\n")
            f.write("import org.springframework.stereotype.Service;\n\n")

            f.write("import java.util.List;\n")
            f.write("import java.util.stream.Collectors;\n\n")
            f.write("import java.util.Collections;\n")
            f.write("import java.util.List;\n")
            f.write("import java.util.Optional;\n")

            f.write(f"@Service\n")
            f.write(f"public class {class_name}ServiceImpl implements {class_name}Service {{\n\n")
            f.write(f"      @Autowired\n")
            f.write(f"      private {class_name}Repository {camel_case(table_name)}Repository;\n\n")

            f.write(f"      @Override\n")
            f.write(f"      public List<{class_name}DTO> findAll() {{\n")
            f.write(f"          List<{class_name}> {camel_case(table_name)} = {camel_case(table_name)}Repository.findAll();\n")
            f.write(f"          return {camel_case(table_name)}.stream().map({class_name}DTO::convertToDTO).collect(Collectors.toList());\n")
            f.write(f"      }}\n")

            f.write(f"      @Override\n")
            f.write(f"      public List<{class_name}DTO> findById(Long id){{\n")
            f.write(f"          Optional<{class_name}> {camel_case(table_name)} = {camel_case(table_name)}Repository.findById(id);\n")
            f.write(f"          return {camel_case(table_name)}.map(f -> Collections.singletonList({class_name}DTO.convertToDTO(f))).orElse(Collections.emptyList());\n")
            f.write("      }\n\n")

            f.write(f"      @Override\n")
            f.write(f"      public {class_name}DTO update(Long id, {class_name}DTO dto) {{\n")
            f.write(f"          Optional<{class_name}> existingEntity = {camel_case(table_name)}Repository.findById(id);\n")
            f.write(f"          if (existingEntity.isPresent()) {{\n")
            f.write(f"              {class_name} entity = existingEntity.get();\n")
            for column in db_structure[table_name]['columns']:
                column_name = column['name']
                java_type = map_sql_type_to_java(column['type'])
                if column_name in many: continue
                f.write(f"              entity.set{pascal_case(column_name)}(dto.get{pascal_case(column_name)}());\n")
            f.write(f"              {camel_case(table_name)}Repository.save(entity);\n")
            f.write(f"              return {class_name}DTO.convertToDTO(entity);\n")
            f.write(f"          } else {{\n")
            f.write(f"              throw new ResourceNotFoundException(\"Entity with id \" + id + \" not found\");\n")
            f.write(f"          }}\n")
            f.write(f"      }}\n\n")

            f.write("}\n")

        print(f"Service implementation {class_name}ServiceImpl.java generated successfully.")

    except Exception as e:
        print(f"Error generating service classes: {e}")
