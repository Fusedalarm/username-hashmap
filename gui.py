import tkinter as tk
from tkinter import messagebox, ttk 
from pipeline import Pipeline


class RootApp:

    def __init__(self, root):
        self.root = root
        self.main_ui()
        self.write_msg("program initialising...")
        self.pipeline = Pipeline()
        self.write_msg("program initialised")
        self.msg = "Alpha 2.0 (Expect bugs program WIP)"
        self.write_msg(self.msg)

    
    def main_ui(self):
        self.root.title("Database")
        self.root.geometry("900x700")
        self.root.config(bg="#f5f5f5")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        
        log_frame = ttk.LabelFrame(self.root, text="Log ", padding=10)
        log_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        self.text_box = tk.Text(
            log_frame,
            height=30,
            width=100,
            font=("Consolas", 9),
            bg="#ffffff",
            fg="#2c3e50",
            relief="flat",
            padx=10,
            pady=10,
            state="disabled"
        )
        self.text_box.grid(row=0, column=0, sticky="nsew")
        
        action_frame = ttk.LabelFrame(self.root, text=" Actions ", padding=15)
        action_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        ttk.Button(action_frame, text="Retrieve", command=lambda: self.open_child_window("r")).pack(side="left", padx=(0, 10))
        ttk.Button(action_frame, text="Map", command= lambda: self.open_child_window("m")).pack(side="left", padx=(0, 10))
        ttk.Button(action_frame, text="Options", command= lambda: self.open_child_window("s")).pack(side="left", padx=(0, 10))
        ttk.Button(action_frame, text="Clear Screen", command=self.clear_screen).pack(side="left", padx=(0, 10))
        ttk.Button(action_frame, text="Exit", command=self.exit_program).pack(side="left")

    def write_msg(self, message):
        self.message = message
        self.text_box.config(state="normal")
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.config(state="disabled")
        self.text_box.see(tk.END)
        
    def clear_screen(self):
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.config(state="disabled")
        self.write_msg(self.msg)

    
    def exit_program(self):
        self.root.destroy()

    # def get_value(self, entry, data_name):
    #     self.entry = entry
    #     self.data_name = data_name
    #     a = entry
    #     a = PreCalculator.entry_fill_validator(a, data_name, self)
    #     if a is not None:
    #         a = PreCalculator.entry_numeric_validator(a, data_name, self)
    #         return a
    #     else:
    #         return None

    
    def open_child_window(self, selector):
        self.selector = selector
        if self.selector == "r":
            RetrieveWindow(self.root, self)
        elif self.selector == "m":
            MapWindow(self.root, self)
        elif self.selector == "s":
            StatWindow(self.root, self)

class RetrieveWindow:
    def __init__(self, parent, app):
        self.window = tk.Toplevel(parent)
        self.app = app

        self.window.title("Retrieve")
        self.window.geometry("250x166")
        self.window.config(bg="#f5f5f5")
        
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        content_frame = ttk.Frame(self.window)
        content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        content_frame.grid_columnconfigure(0, weight=1)
        
        db_frame = ttk.LabelFrame(content_frame, text="Retrieval Key: ", padding=15)
        db_frame.grid(row=1, column=0, sticky="ew")
        db_frame.grid_columnconfigure(0, weight=1)
        
        self.retrieve_entry = ttk.Entry(db_frame, width=40)
        self.retrieve_entry.grid(row=0, column=0, sticky="w", pady=(0, 8))


        ttk.Button(db_frame, text="Enter", command=lambda: self.retrieve_value(self.retrieve_entry) ).grid(row=1, column=0, sticky="ew", pady=(0, 8))
        ttk.Button(db_frame, text="Close", command=self.close).grid(row=2, column=0, sticky="ew")

    def close(self):
        self.window.destroy()
    
    def retrieve_value(self, entry):
        self.entry = entry
        key = self.entry.get().strip()
        if key != "" and key is not None:
            key = self.app.pipeline.retrieve_key(key)
            self.app.write_msg(key)
            self.window.destroy()
        else:
            self.app.write_msg("nothing has been entered")
            
class MapWindow:
    def __init__(self, parent, app):
        self.window = tk.Toplevel(parent)
        self.app = app

        self.window.title("Map")
        self.window.geometry("250x253")
        self.window.config(bg="#f5f5f5")
        
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        content_frame = ttk.Frame(self.window)
        content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        content_frame.grid_columnconfigure(0, weight=1)
        
        db_frame = ttk.LabelFrame(content_frame, text="Map", padding=15)
        db_frame.grid(row=1, column=0, sticky="ew")
        db_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(db_frame, text="Key").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.key_entry = ttk.Entry(db_frame, width=40)
        self.key_entry.grid(row=1, column=0, sticky="w", pady=(0, 8))

        ttk.Label(db_frame, text="Value").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.value_entry = ttk.Entry(db_frame, width=40)
        self.value_entry.grid(row=3, column=0, sticky="w", pady=(0, 8))


        ttk.Button(db_frame, text="Enter", command=lambda: self.map_value(self.key_entry, self.value_entry)).grid(row=4, column=0, sticky="ew", pady=(0, 8))
        ttk.Button(db_frame, text="Close", command=self.close).grid(row=5, column=0, sticky="ew")

    def close(self):
        self.window.destroy()
    
    def map_value(self, key, value):
        self.key = key
        self.value = value
        key = self.key.get().strip()
        value = self.value.get().strip()
        if key == "" or key is None:
            self.app.write_msg("'key' entry is empty")
        if value == "" or value is None:
            self.app.write_msg("'value' entry is empty")
        else:
            return_value = self.app.pipeline.value_input(key, value)
            self.window.destroy()
            self.app.write_msg(return_value)

class StatWindow:
    def __init__(self, parent, app):
        self.window = tk.Toplevel(parent)
        self.app = app

        self.window.title("Stats")
        self.window.geometry("250x155")
        self.window.config(bg="#f5f5f5")
        
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        content_frame = ttk.Frame(self.window)
        content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        content_frame.grid_columnconfigure(0, weight=1)
        
        db_frame = ttk.LabelFrame(content_frame, text="Statistics", padding=15)
        db_frame.grid(row=1, column=0, sticky="ew")
        db_frame.grid_columnconfigure(0, weight=1)
        
        # test = tk.StringVar(value=Pipeline().array_update)
        ttk.Label(db_frame, text="Map size: ").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 0))
        ttk.Label(db_frame, text="Congestion: ").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        ttk.Label(db_frame, text="Hash count: ").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(10, 0))

        ttk.Label(db_frame, text=self.app.pipeline.ARRAY_SIZE).grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(0, 0))
        ttk.Label(db_frame, text=self.app.pipeline.map_congestion).grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(10, 0))
        ttk.Label(db_frame, text=self.app.pipeline.hash_count).grid(row=2, column=1, sticky="w", padx=(0, 10), pady=(10, 0))
    def close(self):
        self.window.destroy()

