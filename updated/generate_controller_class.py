def generate_controller_class(db_structure, output_dir, table_index, package_name):
    try:
        table_name = list(db_structure.keys())[table_index]
        class_name = pascal_case(table_name)

        # Create controller directory
        controller_dir = os.path.join(output_dir, 'controller')
        os.makedirs(controller_dir, exist_ok=True)
        print(f"Controller directory created: {controller_dir}")

        # Generate Controller Class
        controller_path = os.path.join(controller_dir, f"{class_name}Controller.java")
        with open(controller_path, 'w') as f:
            f.write(f"package {package_name}.controller;\n\n")
            f.write(f"import {package_name}.dto.{class_name}DTO;\n")
            f.write(f"import {package_name}.service.{class_name}Service;\n")
            f.write(f"import org.springframework.beans.factory.annotation.Autowired;\n")
            f.write(f"import org.springframework.web.bind.annotation.*;\n\n")
            f.write(f"import java.util.List;\n\n")
            f.write(f"@RestController\n")
            f.write(f"@RequestMapping(\"/{table_name}\")\n")
            f.write(f"public class {class_name}Controller {{\n\n")
            f.write(f"      @Autowired\n")
            f.write(f"      private {class_name}Service {camel_case(table_name)}Service;\n\n")
            f.write(f"      @GetMapping\n")
            f.write(f"      public List<{class_name}DTO> findAll() {{\n")
            f.write(f"          return {camel_case(table_name)}Service.findAll();\n")
            f.write("      }\n")
            f.write(f"      @GetMapping(\"/{{id}}\")\n")
            f.write(f"      public List<{class_name}DTO> findById(@PathVariable Long id){{\n")
            f.write(f"          List<{class_name}DTO> {camel_case(table_name)} = {camel_case(table_name)}Service.findById(id);\n")
            f.write(f"          return {camel_case(table_name)}.isEmpty() ? null : {camel_case(table_name)};\n")
            f.write("      }\n\n")
            f.write(f"      @PutMapping(\"/{{id}}\")\n")
            f.write(f"      public {class_name}DTO update(@PathVariable Long id, @RequestBody {class_name}DTO dto) {{\n")
            f.write(f"          return {camel_case(table_name)}Service.update(id, dto);\n")
            f.write("      }\n\n")

            f.write("}\n")

        print(f"Controller class {class_name}Controller.java generated successfully.")
    
    except Exception as e:
        print(f"Error generating controller class: {e}")
