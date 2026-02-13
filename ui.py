import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import threading
import sys
import re
from pathlib import Path
from PIL import Image
import io
import requests
from typing import Optional

import civitai_fetch_model
import civitai_api_helper as api_helper
from config import ConfigManager


# =========================================================
# GLOBALE KONFIGURATION
# =========================================================

config = ConfigManager()

# Model Metadata (filled in fetch_versions)
current_model_metadata: Optional[dict] = None

# TK Variables (defined later)
root: Optional[tk.Tk] = None


class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.after(0, self._append, message)

    def _append(self, message):
        self.text_widget.configure(state="normal")

        tag = "INFO"
        if message.startswith("[OK]"):
            tag = "OK"
        elif message.startswith("[WARN]"):
            tag = "WARN"
        elif message.startswith("[ERROR]"):
            tag = "ERROR"

        self.text_widget.insert("end", message, tag)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass


def log_clear():
    log_text.configure(state="normal")
    log_text.delete("1.0", tk.END)
    log_text.configure(state="disabled")


# -------------------------------
# Cancel Event (global)
# -------------------------------
cancel_event = threading.Event()


# -------------------------------
# Worker Thread für Fetch
# -------------------------------
def worker(model_id: int, version: str, md_output_dir: Optional[Path] = None, img_output_dir: Optional[Path] = None):
    try:
        print(f"[INFO] Starting fetch for model {model_id} / Version {version}")

        # Fallback to config paths if None
        md_dir = md_output_dir or config.get_path("model_output_dir")
        img_dir = img_output_dir or config.get_path("image_output_dir")

        civitai_fetch_model.run(
            model_id,
            version,
            progress_callback=progress_callback,
            cancel_event=cancel_event,
            md_output_dir=md_dir,
            img_output_dir=img_dir
        )

        if cancel_event.is_set():
            print("[WARN] Process was cancelled")
        else:
            progress_var.set(100)
            print("[OK] Process completed")

    except Exception as e:
        err = str(e)
        print(f"[ERROR] {err}")
        if root:
            root.after(0, lambda err=err: messagebox.showerror("Error", err))

    finally:
        if root:
            root.after(0, lambda: start_button.config(state="normal"))
            root.after(0, lambda: cancel_button.config(state="disabled"))


# -------------------------------
# -------------------------------
# Start Button Logic
# -------------------------------
# -------------------------------
def start_script():
    log_clear()

    try:
        input_value = entry_model.get().strip()
        if not input_value:
            raise ValueError("Please enter model ID or link")

        match = re.search(r"(\d+)", input_value)
        if not match:
            raise ValueError("Invalid model ID or link")

        model_id = int(match.group(1))

        version = dropdown_var.get()
        if version == "Select version" or not version:
            raise ValueError("Please select a version")

        cancel_event.clear()
        progress_var.set(0)

        start_button.config(state="disabled")
        cancel_button.config(state="normal")

        # Get paths from config
        md_output_dir = config.get_path("model_output_dir")
        img_output_dir = config.get_path("image_output_dir")

        threading.Thread(
            target=worker,
            args=(model_id, version, md_output_dir, img_output_dir),
            daemon=True
        ).start()

    except Exception as e:
        start_button.config(state="normal")
        cancel_button.config(state="disabled")
        print(f"[ERROR] {e}")
        messagebox.showerror("Error", str(e))


# -------------------------------
# Cancel Button
# -------------------------------
def cancel_script():
    cancel_event.set()
    print("[WARN] Cancellation requested...")


# -------------------------------
# Version Fetch
# -------------------------------
def fetch_versions():
    global current_model_metadata
    
    log_clear()

    input_value = entry_model.get().strip()
    if not input_value:
        messagebox.showerror("Error", "Please enter model ID or link")
        return

    match = re.search(r"(\d+)", input_value)
    if not match:
        messagebox.showerror("Error", "Invalid model ID or link")
        return

    model_id = int(match.group(1))
    print(f"[INFO] Model ID recognized: {model_id}")

    fetch_versions_button.config(state="disabled")
    version_dropdown.config(state="disabled")
    dropdown_var.set("Select version")

    def thread_func():
        global current_model_metadata
        try:
            metadata = api_helper.get_model_metadata(model_id)
            current_model_metadata = metadata
            
            versions = metadata.get("versions", [])
            if not versions:
                print("[WARN] No versions found")
                return

            print(f"[OK] {len(versions)} versions found")
            model_name = metadata.get("name", "Unknown")
            print(f"[OK] Model: {model_name}")
            
            if root:
                root.after(0, lambda: update_dropdown(versions, metadata))

        except Exception as e:
            print(f"[ERROR] {e}")
            if root:
                root.after(0, lambda: messagebox.showerror("Error", str(e)))

        finally:
            if root:
                root.after(0, lambda: fetch_versions_button.config(state="normal"))

    threading.Thread(target=thread_func, daemon=True).start()


def update_dropdown(versions_list: list[str], metadata: Optional[dict] = None):
    """Update dropdown with versions and display model info if metadata provided."""
    menu = version_dropdown["menu"]
    menu.delete(0, "end")

    for v in versions_list:
        menu.add_command(label=v, command=lambda value=v: dropdown_var.set(value))

    version_dropdown.config(state="normal")
    dropdown_var.set(versions_list[0])
    
    # Update model info display if metadata provided
    if metadata:
        update_model_info(metadata)


def update_model_info(metadata: dict):
    """Update model name, type and thumbnail image display."""
    try:
        # Update model name label
        model_name = metadata.get("name", "Unknown")
        model_type = metadata.get("type", "")
        model_info_text = f"{model_name}"
        if model_type:
            model_info_text += f" ({model_type})"
        
        model_name_label.config(text=model_info_text)
        
        # Update thumbnail image
        image_url = metadata.get("image", "")
        if image_url:
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()
                
                img = Image.open(io.BytesIO(response.content))
                # Resize to 200x200
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                
                # Display thumbnail as text instead of PhotoImage
                # (tk.PhotoImage has compatibility issues with BytesIO)
                model_thumbnail_label.config(text="✓ Image loaded")
                
            except Exception as e:
                model_thumbnail_label.config(text="Image not available")
                print(f"[WARN] Thumbnail could not be loaded: {e}")
        else:
            model_thumbnail_label.config(text="")
            
    except Exception as e:
        print(f"[ERROR] Model info could not be updated: {e}")


# -------
# Progress Bar Callback
# -------
def progress_callback(percent: float):
    def ui_update():
        progress_var.set(percent)
    if root:
        root.after(0, ui_update)


# =========================================================
# UI SETUP
# =========================================================

root = tk.Tk()
root.title("AI Model Fetcher - v0.1.0-beta")
root.geometry("750x750")

# Create notebook (tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=5, pady=5)

# =========================================================
# TAB 1: FETCH
# =========================================================
fetch_frame = ttk.Frame(notebook)
notebook.add(fetch_frame, text="📥 Fetch")

tk.Label(fetch_frame, text="Model ID or API link", font=("Arial", 10)).pack(pady=(10, 2))

# Input frame with entry and fetch button
input_frame = tk.Frame(fetch_frame)
input_frame.pack(pady=(0, 10), padx=10, fill="x")

entry_model = tk.Entry(input_frame, width=50, font=("Arial", 10))
entry_model.pack(side="left", fill="x", expand=True, padx=(0, 5))

fetch_versions_button = tk.Button(
    input_frame,
    text="↻ Fetch",
    command=fetch_versions,
    width=15
)
fetch_versions_button.pack(side="left", padx=(0, 0))

# Model Info Frame
model_info_frame = tk.LabelFrame(fetch_frame, text="Model Information", padx=10, pady=10)
model_info_frame.pack(pady=10, padx=10, fill="x")

model_name_label = tk.Label(model_info_frame, text="", font=("Arial", 11, "bold"))
model_name_label.pack(side="left", padx=10)

model_thumbnail_label = tk.Label(model_info_frame, text="", font=("Arial", 9))
model_thumbnail_label.pack(side="right", padx=10)

# Version Selection
tk.Label(fetch_frame, text="Version", font=("Arial", 10)).pack(pady=(10, 2))

version_frame = tk.Frame(fetch_frame)
version_frame.pack(pady=5)

dropdown_var = tk.StringVar(root)
dropdown_var.set("Select version")

version_dropdown = tk.OptionMenu(version_frame, dropdown_var, "Select version")
version_dropdown.pack(side="left", padx=5)

# Control Buttons
button_frame = tk.Frame(fetch_frame)
button_frame.pack(pady=10)

start_button = tk.Button(
    button_frame,
    text="▶ Start",
    width=15,
    command=start_script
)
start_button.pack(side="left", padx=5)

cancel_button = tk.Button(
    button_frame,
    text="⏹ Cancel",
    width=15,
    state="disabled",
    command=cancel_script
)
cancel_button.pack(side="left", padx=5)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(fetch_frame, variable=progress_var, maximum=100)
progress_bar.pack(fill="x", padx=10, pady=(10, 5))

# Log Output
tk.Label(fetch_frame, text="📋 Console Log", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 2))

log_frame = tk.Frame(fetch_frame)
log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

scrollbar = tk.Scrollbar(log_frame)
scrollbar.pack(side="right", fill="y")

log_text = tk.Text(
    log_frame,
    height=12,
    yscrollcommand=scrollbar.set,
    bg="#1e1e1e",
    fg="#dcdcdc",
    insertbackground="white",
    state="disabled",
    wrap="word",
    font=("Courier", 9)
)
log_text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=log_text.yview)

# =========================================================
# TAB 2: SETTINGS
# =========================================================
settings_frame = ttk.Frame(notebook)
notebook.add(settings_frame, text="⚙️ Settings")

# Path Settings
paths_frame = tk.LabelFrame(settings_frame, text="Storage Paths", padx=15, pady=15)
paths_frame.pack(fill="x", padx=10, pady=10)

# Model Output Path
tk.Label(paths_frame, text="Markdown Output Directory:").pack(anchor="w", pady=(10, 2))
model_output_row = tk.Frame(paths_frame)
model_output_row.pack(fill="x", pady=(0, 10))

model_output_var = tk.StringVar(value=config.get("model_output_dir"))
model_output_entry = tk.Entry(model_output_row, textvariable=model_output_var, width=50)
model_output_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

def browse_model_dir():
    dirname = filedialog.askdirectory(title="Markdown output location")
    if dirname:
        model_output_var.set(dirname)

browse_model_btn = tk.Button(model_output_row, text="Browse", command=browse_model_dir, width=12)
browse_model_btn.pack(side="left", padx=0)

# Image Output Path
tk.Label(paths_frame, text="Image Output Directory:").pack(anchor="w", pady=(10, 2))
image_output_row = tk.Frame(paths_frame)
image_output_row.pack(fill="x", pady=(0, 10))

image_output_var = tk.StringVar(value=config.get("image_output_dir"))
image_output_entry = tk.Entry(image_output_row, textvariable=image_output_var, width=50)
image_output_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

def browse_image_dir():
    dirname = filedialog.askdirectory(title="Image Output location")
    if dirname:
        image_output_var.set(dirname)

browse_image_btn = tk.Button(image_output_row, text="Browse", command=browse_image_dir, width=12)
browse_image_btn.pack(side="left", padx=0)

# Save Button
def save_settings():
    try:
        config.set("model_output_dir", model_output_var.get())
        config.set("image_output_dir", image_output_var.get())
        config.save()
        print("[OK] Settings saved!")
        messagebox.showinfo("Success", "Settings saved!")
    except Exception as e:
        print(f"[ERROR] {e}")
        messagebox.showerror("Error", f"Settings could not be saved: {e}")

save_btn = tk.Button(settings_frame, text="💾 Save", command=save_settings, width=20, font=("Arial", 10, "bold"))
save_btn.pack(pady=20)

# Info Text
info_text = "Paths can be absolute or relative (.).\nChanges will be applied after saving."
info_label = tk.Label(settings_frame, text=info_text, fg="#888888", font=("Arial", 8), justify="left")
info_label.pack(anchor="w", padx=10, pady=10)

# =========================================================
# Tags & Logging
# =========================================================
log_text.tag_config("INFO", foreground="#dcdcdc")
log_text.tag_config("OK", foreground="#00ff00")
log_text.tag_config("WARN", foreground="#ffcc00")
log_text.tag_config("ERROR", foreground="#ff4c4c")

# Redirect stdout/stderr to log
sys.stdout = TextRedirector(log_text)
sys.stderr = TextRedirector(log_text)

# Footer
footer_label = tk.Label(root, text="v0.1.0-beta | made with ❤️ by NoHuman", fg="#888888", font=("Arial", 8))
footer_label.pack(anchor="e", padx=10, pady=5)

root.mainloop()

