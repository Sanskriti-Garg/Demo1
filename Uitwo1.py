import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import threading
import time
import json
from jsonschema import validate, ValidationError

LARGEFONT = ("Verdana", 35)

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Database Schema Generator")
        self.geometry("1200x600")

        # Create a container for the frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        self.frames = {}

        # Create and add frames to the container
        self.frames[StartPage] = StartPage(container, self)
        self.frames[StartPage].grid(row=0, column=0, sticky="nsew")

        self.frames[Page2] = Page2(container, self)
        self.frames[Page2].grid(row=0, column=1, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.is_schema_valid = False

        # Banner section
        banner_frame = tk.Frame(self, bg="red")
        banner_frame.pack(fill=tk.X)
        banner_label = tk.Label(banner_frame, text="WELLS FARGO", bg="red", fg="yellow", font=("Helvetica", 24))
        banner_label.pack(side=tk.LEFT, padx=10)
        yellow_banner = tk.Label(self, bg="yellow", height=1)
        yellow_banner.pack(fill=tk.X, pady=0)

        # Database connection section
        conn_frame = tk.Frame(self)
        conn_frame.pack(fill=tk.X, pady=5)
        db_label = tk.Label(conn_frame, text="Database connection string:")
        db_label.pack(side=tk.LEFT, padx=5)
        self.conn_entry = tk.Entry(conn_frame, width=70)
        self.conn_entry.pack(side=tk.LEFT, padx=5)
        connect_btn = tk.Button(conn_frame, text="Connect", command=self.connect_db)
        connect_btn.pack(side=tk.LEFT, padx=5)

        # JSON Schema Editor
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Icon buttons section
        icon_frame = tk.Frame(self)
        icon_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        import_img = ImageTk.PhotoImage(Image.open("/path/to/import.png").resize((40, 40)))
        edit_img = ImageTk.PhotoImage(Image.open("/path/to/edit.png").resize((40, 40)))
        download_img = ImageTk.PhotoImage(Image.open("/path/to/download.png").resize((40, 40)))
        import_btn = tk.Button(icon_frame, image=import_img, command=self.import_schema)
        import_btn.image = import_img
        import_btn.pack(pady=5)
        edit_btn = tk.Button(icon_frame, image=edit_img, command=self.edit_json)
        edit_btn.image = edit_img
        edit_btn.pack(pady=5)
        download_btn = tk.Button(icon_frame, image=download_img, command=self.download_schema)
        download_btn.image = download_img
        download_btn.pack(pady=5)

        # Action buttons section
        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5, padx=10)
        save_btn = tk.Button(btn_frame, text="Save", command=self.save_schema, width=12, height=2)
        save_btn.pack(side=tk.LEFT, padx=5)
        generate_btn = tk.Button(btn_frame, text="Generate", command=self.check_and_generate, width=12, height=2)
        generate_btn.pack(side=tk.LEFT, padx=5)
        reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_text, width=12, height=2)
        reset_btn.pack(side=tk.LEFT, padx=5)
        compile_btn = tk.Button(btn_frame, text="Compile", command=self.compile_schema, width=12, height=2)
        compile_btn.pack(side=tk.LEFT, padx=5)

    def connect_db(self):
        conn_str = self.conn_entry.get()
        messagebox.showinfo("Connect", f"Connecting to: {conn_str}")

    def save_schema(self):
        self.schema = self.text_area.get("1.0", tk.END)
        messagebox.showinfo("Save", "Schema saved within the application.")

    def check_and_generate(self):
        if not self.text_area.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "Please import the schema first.")
        elif not self.is_schema_valid:
            messagebox.showerror("Error", "Please compile the schema first.")
        else:
            self.controller.frames[Page2].reset_loading()
            threading.Thread(target=self.generate_classes).start()

    def generate_classes(self):
        loading_messages = [
            "Creating Java classes...",
            "Now calling the API...",
            "Processing data...",
            "Almost done..."
        ]
        for message in loading_messages:
            self.controller.frames[Page2].update_loading_message(message)
            time.sleep(2)
        self.controller.frames[Page2].display_final_message()

    def reset_text(self):
        self.text_area.delete("1.0", tk.END)
        self.is_schema_valid = False

    def import_schema(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                schema = file.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, schema)
            self.is_schema_valid = False

    def edit_json(self):
        self.text_area.config(state=tk.NORMAL)

    def download_schema(self):
        schema = self.text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(schema)
            messagebox.showinfo("Download", f"Schema downloaded to: {file_path}")

    def compile_schema(self):
        schema_text = self.text_area.get("1.0", tk.END).strip()
        if not schema_text:
            messagebox.showerror("Compile", "The schema is empty.")
            return

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
                                    "default": {},
                                    "autoincrement": {"type": "boolean"},
                                    "comment": {},
                                    "identity": {
                                        "type": "object",
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
                                    "constrained_columns": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "references": {
                                        "type": "object",
                                        "properties": {
                                            "table": {"type": "string"},
                                            "columns": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            }
                                        },
                                        "required": ["table", "columns"]
                                    }
                                },
                                "required": ["name", "constrained_columns", "references"]
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
                                    }
                                },
                                "required": ["name", "columns"]
                            }
                        }
                    },
                    "required": ["columns", "primary_keys"]


              try:
        schema_data = json.loads(schema_text)
        validate(instance=schema_data, schema=example_schema)
        messagebox.showinfo("Compile", "Schema is valid.")
        self.is_schema_valid = True
    except json.JSONDecodeError as e:
        messagebox.showerror("Compile", f"Invalid JSON: {str(e)}")
        self.is_schema_valid = False
    except ValidationError as e:
        messagebox.showerror("Compile", f"Schema validation error: {str(e)}")
        self.is_schema_valid = False
 }
            },
            "required": ["TableName"]
        }

        try:
            schema_data = json.loads(schema_text)
            validate(instance=schema_data, schema=example_schema)
            messagebox.showinfo("Compile", "Schema is valid.")
            self.is_schema_valid = True
        except json.JSONDecodeError as e:
            messagebox.showerror("Compile", f"Invalid JSON: {str(e)}")
            self.is_schema_valid = False
        except ValidationError as e:
            messagebox.showerror("Compile", f"Schema validation error: {str(e)}")
            self.is_schema_valid = False

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.loading_label = tk.Label(self, text="Creating the Java classes", font=LARGEFONT)
        self.loading_label.pack(pady=10, padx=10)

    def update_loading_message(self, message):
        self.loading_label.config(text=message)

    def display_final_message(self):
        self.loading_label.config(text="Java classes generated successfully.")

    def reset_loading(self):
        self.loading_label.config(text="Creating the Java classes")

# Driver Code
app = tkinterApp()
app.mainloop()
