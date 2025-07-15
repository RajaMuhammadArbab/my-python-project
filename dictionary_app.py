import tkinter as tk
from tkinter import messagebox
import os

# Dictionary file name
DICT_FILE = "dictionary.txt"

# Load dictionary from file
def load_dictionary():
    dictionary = {}
    if os.path.exists(DICT_FILE):
        with open(DICT_FILE, "r", encoding='utf-8') as file:
            for line in file:
                if ":" in line:
                    word, meaning = line.strip().split(":", 1)
                    dictionary[word.lower()] = meaning
    return dictionary

# Save a new word to the file
def save_word(word, meaning):
    with open(DICT_FILE, "a", encoding='utf-8') as file:
        file.write(f"{word}:{meaning}\n")

# Search for word meaning
def search_word():
    word = word_entry.get().strip().lower()
    if word in dictionary:
        result_label.config(text=f"Meaning: {dictionary[word]}")
    else:
        result_label.config(text="Word not found in dictionary.")

# Add a new word
def add_word():
    new_word = new_word_entry.get().strip().lower()
    new_meaning = new_meaning_entry.get().strip()

    if new_word == "" or new_meaning == "":
        messagebox.showwarning("Input Error", "Both fields are required.")
        return

    if new_word in dictionary:
        messagebox.showinfo("Duplicate", "Word already exists in the dictionary.")
    else:
        dictionary[new_word] = new_meaning
        save_word(new_word, new_meaning)
        messagebox.showinfo("Success", f"'{new_word}' added to the dictionary.")
        new_word_entry.delete(0, tk.END)
        new_meaning_entry.delete(0, tk.END)

# Initialize dictionary
dictionary = load_dictionary()

# Create GUI window
root = tk.Tk()
root.title("Word Meaning Dictionary")
root.geometry("400x400")
root.resizable(False, False)

# Word search
tk.Label(root, text="Enter a word to search:", font=('Arial', 12)).pack(pady=5)
word_entry = tk.Entry(root, width=30)
word_entry.pack()

tk.Button(root, text="Search", command=search_word).pack(pady=5)
result_label = tk.Label(root, text="", font=('Arial', 12), fg='blue')
result_label.pack(pady=10)

# Add new word section
tk.Label(root, text="Add New Word", font=('Arial', 14, 'bold')).pack(pady=10)
tk.Label(root, text="Word:", font=('Arial', 12)).pack()
new_word_entry = tk.Entry(root, width=30)
new_word_entry.pack()

tk.Label(root, text="Meaning:", font=('Arial', 12)).pack()
new_meaning_entry = tk.Entry(root, width=30)
new_meaning_entry.pack()

tk.Button(root, text="Add Word", command=add_word).pack(pady=10)

# Run the GUI
root.mainloop()
