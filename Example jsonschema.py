def compile_schema(self):
    schema_text = self.text_area.get("1.0", tk.END).strip()
    example_schema = {
        "type": "object",
        "properties": {
            "TableName": {
                "type": "object",
                "properties": {
                    "columns": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string"},
                                "nullable": {"type": "boolean"},
                                "default": {"type": ["string", "null"]},
                                "autoincrement": {"type": "boolean"},
                                "comment": {"type": ["string", "null"]},
                                "identity": {
                                    "type": ["object", "null"],
                                    "properties": {
                                        "start": {"type": "integer"},
                                        "increment": {"type": "integer"}
                                    },
                                    "required": ["start", "increment"]
                                }
                            },
                            "required": ["name", "type"]
                        }
                    },
                    "primary_keys": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "constrained_columns": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["name", "constrained_columns"]
                    },
                    "foreign_keys": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "columns": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "referenced_table": {"type": "string"},
                                "referenced_columns": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            }
                        }
                    },
                    "indexes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "columns": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "unique": {"type": "boolean"}
                            }
                        }
                    }
                },
                "required": ["columns", "primary_keys"]
            }
        },
        "required": ["TableName"]
    }

    schema_text = schema_text.rstrip()
    try:
        schema = json.loads(schema_text)
        validate(instance=schema, schema=example_schema)
        messagebox.showinfo("Compile", "JSON schema is valid!")
        self.is_schema_valid = True
    except json.JSONDecodeError as e:
        messagebox.showerror("Compile Error", f"Invalid JSON: {e}")
        self.is_schema_valid = False
    except ValidationError as e:
        messagebox.showerror("Compile Error", f"Schema validation error: {e.message}")
        self.is_schema_valid = False
    except Exception as e:
        messagebox.showerror("Compile Error", f"An unexpected error occurred: {e}")
        self.is_schema_valid = False
