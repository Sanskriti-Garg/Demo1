import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from tkinter import simpledialog
import json

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Schema Generator")
        self.root.geometry("800x600")
        self.schema = ""
        self.create_widgets()

    def create_widgets(self):
        # Wells Fargo banner with logo
        banner_frame = tk.Frame(self.root, bg="red")
        banner_frame.pack(fill=tk.X)

        logo = tk.PhotoImage(file="wells_fargo_logo.png")
        logo_label = tk.Label(banner_frame, image=logo, bg="red")
        logo_label.image = logo  # keep a reference!
        logo_label.pack(side=tk.LEFT, padx=10, pady=5)

        banner_label = tk.Label(banner_frame, text="WELLS FARGO", bg="red", fg="white", font=("Helvetica", 24))
        banner_label.pack(side=tk.LEFT, padx=10)

        # Thinner yellow line below the red banner
        yellow_banner = tk.Label(self.root, bg="yellow")
        yellow_banner.pack(fill=tk.X, pady=0, height=1)

        # Database connection string entry
        conn_frame = tk.Frame(self.root)
        conn_frame.pack(fill=tk.X, pady=5)
        self.conn_entry = tk.Entry(conn_frame, width=50)
        self.conn_entry.insert(0, "Database connection string...")
        self.conn_entry.pack(side=tk.LEFT, padx=5)
        connect_btn = tk.Button(conn_frame, text="Connect", command=self.connect_db)
        connect_btn.pack(side=tk.LEFT, padx=5)

        # JSON schema text area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Buttons for Save, Generate, Reset, Import, Edit, Link, Download
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, pady=5)

        save_btn = tk.Button(btn_frame, text="Save", command=self.save_schema)
        save_btn.pack(side=tk.LEFT, padx=5)

        generate_btn = tk.Button(btn_frame, text="Generate", command=self.generate_classes)
        generate_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_text)
        reset_btn.pack(side=tk.LEFT, padx=5)

        # Icons for Import, Edit, Link, Download
        import_icon = tk.PhotoImage(file="import_icon.png")
        edit_icon = tk.PhotoImage(file="edit_icon.png")
        link_icon = tk.PhotoImage(file="link_icon.png")
        download_icon = tk.PhotoImage(file="download_icon.png")

        import_btn = tk.Button(btn_frame, image=import_icon, command=self.import_schema)
        import_btn.image = import_icon
        import_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = tk.Button(btn_frame, image=edit_icon, command=self.edit_json)
        edit_btn.image = edit_icon
        edit_btn.pack(side=tk.LEFT, padx=5)

        link_btn = tk.Button(btn_frame, image=link_icon, command=self.add_link)
        link_btn.image = link_icon
        link_btn.pack(side=tk.LEFT, padx=5)

        download_btn = tk.Button(btn_frame, image=download_icon, command=self.download_schema)
        download_btn.image = download_icon
        download_btn.pack(side=tk.LEFT, padx=5)

    def connect_db(self):
        conn_str = self.conn_entry.get()
        messagebox.showinfo("Connect", f"Connecting to: {conn_str}")

    def save_schema(self):
        self.schema = self.text_area.get("1.0", tk.END)
        messagebox.showinfo("Save", "Schema saved within the application.")

    def generate_classes(self):
        schema = self.text_area.get("1.0", tk.END)
        # Simulate generating Java classes from JSON schema
        messagebox.showinfo("Generate", "Generating Java classes...")

    def reset_text(self):
        self.text_area.delete("1.0", tk.END)

    def import_schema(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                schema = file.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, schema)
            messagebox.showinfo("Import", f"Schema imported from: {file_path}")

    def edit_json(self):
        json_text = self.text_area.get("1.0", tk.END)
        try:
            json_data = json.loads(json_text)
            json_str = json.dumps(json_data, indent=4)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, json_str)
            messagebox.showinfo("Edit", "JSON formatted successfully.")
        except json.JSONDecodeError:
            messagebox.showerror("Edit", "Invalid JSON format.")

    def add_link(self):
        link = simpledialog.askstring("Add Link", "Enter the link:")
        if link:
            self.text_area.insert(tk.END, f'"link": "{link}",\n')

    def download_schema(self):
        schema = self.text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(schema)
            messagebox.showinfo("Download", f"Schema downloaded to: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
