import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import time
import json
import re
from jsonschema import validate, ValidationError
import os

LARGEFONT = ("Verdana", 35)

dark_mode = {
    "bg": "#2e2e2e",
    "fg": "#ffffff",
    "button_bg": "#3e3e3e",
    "button_fg": "#ffffff",
    "entry_bg": "#3e3e3e",
    "entry_fg": "#ffffff",
    "text_bg": "#1e1e1e",
    "text_fg": "#d4d4d4",
    "right_bg": "#2e2e2e",
    "right_fg": "#ffffff"
}

light_mode = {
    "bg": "#ffffff",
    "fg": "#000000",
    "button_bg": "#e0e0e0",
    "button_fg": "#000000",
    "entry_bg": "#f0f0f0",
    "entry_fg": "#000000",
    "text_bg": "#ffffff",
    "text_fg": "#000000",
    "right_bg": "#ffffff",
    "right_fg": "#000000"
}

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Database Schema Generator")
        self.geometry("1800x600")

        # Load sun and moon images
        self.sun_img = ImageTk.PhotoImage(Image.open("sun.png").resize((30, 30)))
        self.moon_img = ImageTk.PhotoImage(Image.open("moon.png").resize((30, 30)))

        # Set default mode to light
        self.current_mode = "light"
        self.apply_theme(light_mode)

        # Create the banner at the top
        banner_frame = tk.Frame(self, bg="red")
        banner_frame.pack(fill=tk.X, pady=0)

        banner_label = tk.Label(banner_frame, text="WELLS FARGO", bg="red", fg="yellow", font=("Helvetica", 24))
        banner_label.pack(side=tk.LEFT, padx=10)

        yellow_banner = tk.Label(self, bg="yellow", height=1)
        yellow_banner.pack(fill=tk.X, pady=0)

        # Mode toggle button
        self.mode_toggle_btn = tk.Button(banner_frame, image=self.moon_img, command=self.toggle_mode, bg="red", borderwidth=0)
        self.mode_toggle_btn.pack(side=tk.RIGHT, padx=10)

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

    def toggle_mode(self):
        if self.current_mode == "light":
            self.current_mode = "dark"
            self.apply_theme(dark_mode)
            self.mode_toggle_btn.config(image=self.sun_img)
        else:
            self.current_mode = "light"
            self.apply_theme(light_mode)
            self.mode_toggle_btn.config(image=self.moon_img)

    def apply_theme(self, theme):
        # Update background and foreground colors
        self.config(bg=theme["bg"])

        for widget in self.winfo_children():
            widget_type = widget.winfo_class()

            if widget_type == "Frame":
                widget.config(bg=theme["bg"])
            elif widget_type == "Label":
                widget.config(bg=theme["bg"], fg=theme["fg"])
            elif widget_type == "Button":
                widget.config(bg=theme["button_bg"], fg=theme["button_fg"])
            elif widget_type == "Entry":
                widget.config(bg=theme["entry_bg"], fg=theme["entry_fg"])
            elif widget_type == "Text":
                widget.config(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"])
            elif widget_type == "TLabel":
                widget.config(background=theme["right_bg"], foreground=theme["right_fg"])

        # Update specific frames or widgets that are not direct children
        self.frames[StartPage].apply_theme(self.current_mode)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Left frame
        left_frame = tk.Frame(self, bg=controller.current_mode)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Connection string label and entry
        self.conn_label = tk.Label(left_frame, text="Enter connection string", font=LARGEFONT, bg=controller.current_mode)
        self.conn_label.pack(pady=10)

        self.conn_entry = tk.Entry(left_frame, font=("Helvetica", 16), bd=2)
        self.conn_entry.pack(pady=10, padx=10)

        self.connect_button = tk.Button(left_frame, text="Connect", font=("Helvetica", 16), command=self.connect)
        self.connect_button.pack(pady=10)

        # JSON Import, Edit, Save, and Compile
        self.import_button = tk.Button(left_frame, text="Import JSON", font=("Helvetica", 16), command=self.import_json)
        self.import_button.pack(pady=10)

        self.edit_button = tk.Button(left_frame, text="Edit JSON", font=("Helvetica", 16), command=self.edit_json)
        self.edit_button.pack(pady=10)

        self.save_button = tk.Button(left_frame, text="Save JSON", font=("Helvetica", 16), command=self.save_json)
        self.save_button.pack(pady=10)

        self.compile_button = tk.Button(left_frame, text="Compile JSON", font=("Helvetica", 16), command=self.compile_json)
        self.compile_button.pack(pady=10)

        # Text area
        self.text_area = tk.Text(left_frame, font=("Helvetica", 16), wrap="word", bd=2, relief="solid")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)

        # Right frame
        self.right_frame = tk.Frame(self, bg=controller.current_mode)
        self.right_frame.pack(side="right", fill="y", padx=(5, 10), pady=10)

        self.output_label = ttk.Label(self.right_frame, text="Output will be displayed here", background=controller.current_mode)
        self.output_label.pack(pady=10)

        # Apply theme initially
        self.apply_theme(controller.current_mode)

    def connect(self):
        # Implement the connect function
        pass

    def import_json(self):
        # Implement the import JSON function
        pass

    def edit_json(self):
        # Implement the edit JSON function
        pass

    def save_json(self):
        # Implement the save JSON function
        pass

    def compile_json(self):
        # Implement the compile JSON function
        pass

    def apply_theme(self, mode):
        theme = dark_mode if mode == "dark" else light_mode

        self.config(bg=theme["bg"])
        self.conn_label.config(bg=theme["bg"], fg=theme["fg"])
        self.conn_entry.config(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["fg"])
        self.text_area.config(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"])
        self.right_frame.config(bg=theme["right_bg"])
        self.output_label.config(background=theme["right_bg"], foreground=theme["right_fg"])
        self.connect_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        self.import_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        self.edit_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        self.save_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        self.compile_button.config(bg=theme["button_bg"], fg=theme["button_fg"])

# Main loop to run the app
app = tkinterApp()
app.mainloop()
