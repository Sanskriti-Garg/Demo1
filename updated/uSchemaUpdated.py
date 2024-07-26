import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        self.geometry("1800x600")  # Adjusted width to fit the split view

        # Create the banner at the top
        banner_frame = tk.Frame(self, bg="red")
        banner_frame.pack(fill=tk.X, pady=0)
        banner_label = tk.Label(banner_frame, text="WELLS FARGO", bg="red", fg="yellow", font=("Helvetica", 24))
        banner_label.pack(side=tk.LEFT, padx=10)
        yellow_banner = tk.Label(self, bg="yellow", height=1)
        yellow_banner.pack(fill=tk.X, pady=0)

        # Create the split view container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True, pady=(0, 10))

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        self.frames = {}

        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.bind("<KeyRelease>", self._on_key_release)

        self.tag_configure("keyword", foreground="orange")
        self.tag_configure("string", foreground="green")
        self.tag_configure("comment", foreground="grey")
        self.tag_configure("number", foreground="blue")
        self.tag_configure("braces", foreground="yellow")
        self.tag_configure("colon", foreground="red")

    def _on_key_release(self, event):
        self._highlight_syntax()

    def _highlight_syntax(self):
        self.remove_tags("1.0", tk.END)
        for pattern, tag in self.get_patterns():
            start = 1.0
            while True:
                pos = self.search(pattern, start, tk.END, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(self.get(pos, pos + ' lineend'))}c"
                self.tag_add(tag, pos, end)
                start = end

    def remove_tags(self, start, end):
        for tag in ["keyword", "string", "comment", "number", "braces", "colon"]:
            self.tag_remove(tag, start, end)

    @staticmethod
    def get_patterns():
        return [
            (r'\b(true|false|null)\b', "keyword"),
            (r'".*?"', "string"),
            (r'//.*', "comment"),
            (r'\b\d+\b', "number"),
            (r'[{}[\]]', "braces"),
            (r':', "colon")
        ]

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")

        self.compiled_successfully = False

        # Left side of the split view
        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        conn_frame = tk.Frame(left_frame)
        conn_frame.grid(row=0, column=0, sticky="ew")

        db_label = tk.Label(conn_frame, text="Database connection string:")
        db_label.pack(side=tk.LEFT, padx=5)

        self.conn_entry = tk.Entry(conn_frame, width=80)  # Increased width
        self.conn_entry.pack(side=tk.LEFT, padx=5, pady=10)
        connect_btn = tk.Button(conn_frame, text="Connect", command=self.connect_db)
        connect_btn.pack(side=tk.LEFT, padx=5, pady=10)

        text_frame = tk.Frame(left_frame)
        text_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))

        self.text_area = CustomText(text_frame, wrap=tk.WORD, width=70, height=40, bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_area.insert(tk.END, "Imported JSON will be shown here.")
        self.text_area.config(state=tk.DISABLED)

        # Icon buttons to the right of the input text field
        icon_frame = tk.Frame(left_frame)
        icon_frame.grid(row=1, column=1, sticky="ns", padx=(5, 0))

        import_img = ImageTk.PhotoImage(Image.open("import.png").resize((40, 40)))
        edit_img = ImageTk.PhotoImage(Image.open("edit.png").resize((40, 40)))
        download_img = ImageTk.PhotoImage(Image.open("download.png").resize((40, 40)))

        import_btn = tk.Button(icon_frame, image=import_img, command=self.import_schema)
        import_btn.image = import_img
        import_btn.pack(pady=5)

        edit_btn = tk.Button(icon_frame, image=edit_img, command=self.edit_json)
        edit_btn.image = edit_img
        edit_btn.pack(pady=5)

        download_btn = tk.Button(icon_frame, image=download_img, command=self.download_schema)
        download_btn.image = download_img
        download_btn.pack(pady=5)

        # Button frame at the bottom
        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5, padx=10)

        save_btn = tk.Button(btn_frame, text="Save", command=self.save_schema, width=12, height=2)
        save_btn.pack(side=tk.LEFT, padx=5)

        self.generate_btn = tk.Button(btn_frame, text="Generate", command=self.check_and_generate, width=12, height=2, state=tk.NORMAL)
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_text, width=12, height=2)
        reset_btn.pack(side=tk.LEFT, padx=5)

        compile_btn = tk.Button(btn_frame, text="Compile", command=self.check_and_compile, width=12, height=2)
        compile_btn.pack(side=tk.LEFT, padx=5)

        # Right side of the split view
        right_frame = tk.Frame(self, bg="#fff")  # Changed background color
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.initial_label = ttk.Label(right_frame, text="Output screen", font=LARGEFONT, background="#fff")
        self.initial_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.loading_label = ttk.Label(right_frame, text="Generating Java classes...", font=LARGEFONT, background="#fff")
        self.progress_bar = ttk.Progressbar(right_frame, mode='indeterminate')
        
        self.output_text = tk.StringVar()
        self.output_label = ttk.Label(right_frame, textvariable=self.output_text, font=LARGEFONT, background="#fff")
        self.output_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def connect_db(self):
        conn_str = self.conn_entry.get()
        messagebox.showinfo("Connect", f"Connecting to: {conn_str}")

    def save_schema(self):
        schema_text = self.text_area.get("1.0", tk.END).strip()
        if schema_text == "Imported JSON will be shown here." or not schema_text:
            messagebox.showwarning("Warning", "Nothing to save.")
            return
        self.schema = schema_text
        messagebox.showinfo("Save", "Schema saved within the application.")

    def check_and_generate(self):
        if not self.compiled_successfully:
            messagebox.showwarning("Warning", "Please compile successfully before generating.")
            return
        self.start_generation()

    def check_and_compile(self):
        schema_text = self.text_area.get("1.0", tk.END).strip()
        if schema_text == "Imported JSON will be shown here." or not schema_text:
            messagebox.showwarning("Warning", "Nothing to compile.")
            return
        self.compile_schema()

    def start_generation(self):
        self.initial_label.place_forget()
        self.loading_label.pack()
        self.progress_bar.pack()
        self.progress_bar.start()
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
        self.loading_label.config(text=message)

    
    def display_final_message(self):
    # Stop and hide the progress bar
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        # Clear and hide the loading label
        self.loading_label.config(text="")
        self.loading_label.pack_forget()

    # Hide the initial label
        self.initial_label.place_forget()

    # Show the final message centered
        self.output_text.set("Data will be shown here")
        self.output_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    

    def reset_text(self):
    # Reset the text area on the left
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", "Imported JSON will be shown here.")
        self.text_area.config(state=tk.DISABLED)

    # Reset the compiled state and generate button
        self.compiled_successfully = False
        self.generate_btn.config(state=tk.DISABLED)
    
    # Reset the right pane to its initial state
        self.initial_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.loading_label.pack_forget()
        self.output_label.pack_forget()
        self.output_text.set("Output Screen")

    def import_schema(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                schema = file.read()
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, schema)
            self.text_area.config(state=tk.DISABLED)

    def edit_json(self):
        schema_text = self.text_area.get("1.0", tk.END).strip()
        if schema_text == "Imported JSON will be shown here." or not schema_text:
            messagebox.showwarning("Warning", "Nothing to edit.")
            return
        self.text_area.config(state=tk.NORMAL)

    def download_schema(self):
        schema_text = self.text_area.get("1.0", tk.END).strip()
        if schema_text == "Imported JSON will be shown here." or not schema_text:
            messagebox.showwarning("Warning", "Nothing to download.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(schema_text)
            messagebox.showinfo("Download", f"Schema downloaded to: {file_path}")

    
    
    def compile_schema(self):
        schema_text = self.text_area.get("1.0", tk.END).strip()
        try:
            json_schema = json.loads(schema_text)
            validate(instance={}, schema=json_schema)  # Validate an empty instance against the schema
            self.compiled_successfully = True
            self.generate_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Compile", "Json schema compiled successfully.")
        except json.JSONDecodeError:
            self.compiled_successfully = False
            messagebox.showerror("Json compiler error", "Invalid JSON format.")
        except ValidationError as e:
            self.compiled_successfully = False
            messagebox.showerror("Json compiler error", f"Schema validation error: {e.message}")
        except Exception as e:
            self.compiled_successfully = False
            messagebox.showerror("Json compiler error", f"Compilation error: {str(e)}")

app = tkinterApp()
app.mainloop()
