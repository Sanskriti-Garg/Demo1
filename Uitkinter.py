import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Schema Generator")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Wells Fargo banner
        banner = tk.Label(self.root, text="WELLS FARGO", bg="red", fg="white", font=("Helvetica", 24))
        banner.pack(fill=tk.X)

        # Database connection string entry
        conn_frame = tk.Frame(self.root)
        conn_frame.pack(fill=tk.X, pady=5)
        conn_label = tk.Label(conn_frame, text="Database connection string...")
        conn_label.pack(side=tk.LEFT, padx=5)
        self.conn_entry = tk.Entry(conn_frame, width=50)
        self.conn_entry.pack(side=tk.LEFT, padx=5)
        connect_btn = tk.Button(conn_frame, text="Connect", command=self.connect_db)
        connect_btn.pack(side=tk.LEFT, padx=5)

        # JSON schema text area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Buttons for Save, Generate, Reset
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, pady=5)
        save_btn = tk.Button(btn_frame, text="Save", command=self.save_schema)
        save_btn.pack(side=tk.LEFT, padx=5)
        generate_btn = tk.Button(btn_frame, text="Generate", command=self.generate_classes)
        generate_btn.pack(side=tk.LEFT, padx=5)
        reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_text)
        reset_btn.pack(side=tk.LEFT, padx=5)

    def connect_db(self):
        conn_str = self.conn_entry.get()
        messagebox.showinfo("Connect", f"Connecting to: {conn_str}")

    def save_schema(self):
        schema = self.text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(schema)
            messagebox.showinfo("Save", f"Schema saved to: {file_path}")

    def generate_classes(self):
        schema = self.text_area.get("1.0", tk.END)
        # Simulate generating Java classes from JSON schema
        messagebox.showinfo("Generate", "Generating Java classes...")

    def reset_text(self):
        self.text_area.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
