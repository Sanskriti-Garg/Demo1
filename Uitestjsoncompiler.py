import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import json
from jsonschema import validate, ValidationError

LARGEFONT = ("Verdana", 35)

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Database Schema Generator")
        self.geometry("900x600")

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        banner_frame = tk.Frame(self, bg="red")
        banner_frame.pack(fill=tk.X)

        banner_label = tk.Label(banner_frame, text="WELLS FARGO", bg="red", fg="yellow", font=("Helvetica", 24))
        banner_label.pack(side=tk.LEFT, padx=10)

        yellow_banner = tk.Label(self, bg="yellow", height=1)
        yellow_banner.pack(fill=tk.X, pady=0)

        conn_frame = tk.Frame(self)
        conn_frame.pack(fill=tk.X, pady=5)

        db_label = tk.Label(conn_frame, text="Database connection string:")
        db_label.pack(side=tk.LEFT, padx=5)

        self.conn_entry = tk.Entry(conn_frame, width=70)
        self.conn_entry.pack(side=tk.LEFT, padx=5)
        connect_btn = tk.Button(conn_frame, text="Connect", command=self.connect_db)
        connect_btn.pack(side=tk.LEFT, padx=5)

        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.text_area.config(state=tk.DISABLED)

        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        import_img = ImageTk.PhotoImage(Image.open("import.png").resize((40, 40)))
        edit_img = ImageTk.PhotoImage(Image.open("edit.png").resize((40, 40)))
        download_img = ImageTk.PhotoImage(Image.open("download.png").resize((40, 40)))

        import_btn = tk.Button(right_frame, image=import_img, command=self.import_schema)
        import_btn.image = import_img
        import_btn.pack(pady=5)

        edit_btn = tk.Button(right_frame, image=edit_img, command=self.edit_json)
        edit_btn.image = edit_img
        edit_btn.pack(pady=5)

        download_btn = tk.Button(right_frame, image=download_img, command=self.download_schema)
        download_btn.image = download_img
        download_btn.pack(pady=5)

        save_btn = tk.Button(right_frame, text="Save", command=self.save_schema, width=12, height=2)
        save_btn.pack(pady=5)

        generate_btn = tk.Button(right_frame, text="Generate", command=self.start_generation, width=12, height=2)
        generate_btn.pack(pady=5)

        reset_btn = tk.Button(right_frame, text="Reset", command=self.reset_text, width=12, height=2)
        reset_btn.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5, padx=10)

        button1 = ttk.Button(self, text="Page 1", command=lambda: controller.show_frame(Page1))
        button1.pack(side=tk.LEFT, padx=10, pady=10)

    def connect_db(self):
        conn_str = self.conn_entry.get()
        messagebox.showinfo("Connect", f"Connecting to: {conn_str}")

    def save_schema(self):
        self.schema = self.text_area.get("1.0", tk.END)
        messagebox.showinfo("Save", "Schema saved within the application.")

    def start_generation(self):
        if not self.is_schema_valid:
            messagebox.showwarning("Generate", "Please compile the schema first.")
            return

        if not self.text_area.get("1.0", tk.END).strip():
            messagebox.showwarning("Generate", "Please import or enter a schema before generating.")
            return

        self.controller.show_frame(Page2)
        threading.Thread(target=self.generate_classes).start()

    def generate_classes(self):
        loading_messages = [
            "Creating Java classes...",
            "Now calling the API...",
            "Processing data...",
            "Almost done..."
        ]
        for message in loading_messages:
            self.update_loading_message(message)
            time.sleep(2)
        self.display_final_message()

    def update_loading_message(self, message):
        self.controller.frames[Page2].loading_label.config(text=message)

    def display_final_message(self):
        self.controller.frames[Page2].progress_bar.stop()
        self.controller.frames[Page2].progress_bar.pack_forget()
        self.controller.frames[Page2].loading_label.config(text="Data will be shown here")

    def reset_text(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)

    def import_schema(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                schema = file.read()
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, schema)
            self.text_area.config(state=tk.DISABLED)
            self.is_schema_valid = False  # Reset validation status

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
                    "required":

 ["columns", "primary_keys"]
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

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="StartPage", command=lambda: controller.show_frame(StartPage))
        button1.pack()

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.loading_label = ttk.Label(self, text="Generating Java classes...", font=LARGEFONT)
        self.loading_label.pack(pady=20)

        self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, padx=20, pady=20)
        self.progress_bar.start()

        back_btn = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_btn.pack(pady=10)

# Driver Code
app = tkinterApp()
app.mainloop()
