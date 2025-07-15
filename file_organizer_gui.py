import os
import shutil
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"]
}


log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "organizer.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def organize_directory(path, recursive=False, dry_run=False):
    moved_files = 0

    for root, _, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isdir(file_path):
                continue

            _, ext = os.path.splitext(filename)
            if not ext:
                continue

            category = get_category(ext)
            target_folder = os.path.join(path, category)
            os.makedirs(target_folder, exist_ok=True)
            target_path = os.path.join(target_folder, filename)

            try:
                if dry_run:
                    print(f"[DRY RUN] Would move: {file_path} -> {target_path}")
                    logging.info(f"[DRY RUN] Would move: {file_path} -> {target_path}")
                else:
                    if os.path.abspath(file_path) != os.path.abspath(target_path):
                        shutil.move(file_path, target_path)
                        print(f"Moved: {file_path} -> {target_path}")
                        logging.info(f"Moved: {file_path} -> {target_path}")
                        moved_files += 1
            except Exception as e:
                logging.error(f"Error moving {file_path} to {target_path}: {e}")

        if not recursive:
            break

    return moved_files


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")

        self.directory_path = tk.StringVar()
        self.recursive = tk.BooleanVar()
        self.dry_run = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
      
        tk.Label(self.root, text="Target Directory:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.root, textvariable=self.directory_path, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_directory).grid(row=0, column=2, padx=5)

       
        tk.Checkbutton(self.root, text="Recursive", variable=self.recursive).grid(row=1, column=1, sticky="w")
        tk.Checkbutton(self.root, text="Dry Run (Preview)", variable=self.dry_run).grid(row=2, column=1, sticky="w")

        
        tk.Button(self.root, text="Organize Files", command=self.run_organizer, bg="#2FC0E4", fg="white").grid(row=3, column=1, pady=20)

    def browse_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.directory_path.set(selected_dir)

    def run_organizer(self):
        directory = self.directory_path.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Invalid Directory", "Please select a valid directory.")
            return

        moved_count = organize_directory(directory, self.recursive.get(), self.dry_run.get())

        if self.dry_run.get():
            messagebox.showinfo("Dry Run Complete", "Preview complete. Check the log file for details.")
        else:
            messagebox.showinfo("Organization Complete", f"Moved {moved_count} files successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
