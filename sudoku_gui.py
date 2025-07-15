import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = np.zeros((9, 9), dtype=int)
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Solve", command=self.solve).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Load", command=self.load_from_file).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Save", command=self.save_to_file).grid(row=0, column=3, padx=5)

    def load_board_from_entries(self):
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                self.board[i][j] = int(val) if val.isdigit() else 0

    def update_entries_from_board(self):
        for i in range(9):
            for j in range(9):
                val = str(self.board[i][j]) if self.board[i][j] != 0 else ""
                entry = self.entries[i][j]
                entry.delete(0, tk.END)
                entry.insert(0, val)
            if self.original_board[i][j] != 0:
                entry.config(fg='black', bg='white', state='readonly')
            else:
                entry.config(fg='black', bg='#b2fab4', state='readonly')  


    def clear(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.update_entries_from_board()

    def solve(self):
        self.load_board_from_entries()
        self.original_board = self.board.copy()
        if solve_sudoku(self.board):
            self.update_entries_from_board()
            messagebox.showinfo("Solved", "Sudoku puzzle solved successfully!")
        else:
            messagebox.showerror("Error", "No solution exists for the given puzzle.")


    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt *.csv")])
        if file_path:
            try:
                data = np.loadtxt(file_path, dtype=int)
                if data.shape == (9, 9):
                    self.board = data
                    self.update_entries_from_board()
                else:
                    messagebox.showerror("Error", "Invalid file format.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file.\n{e}")

    def save_to_file(self):
        self.load_board_from_entries()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt *.csv")])
        if file_path:
            np.savetxt(file_path, self.board, fmt='%d')
            messagebox.showinfo("Saved", f"Board saved to {file_path}")


def is_valid(board, row, col, num):
    if num in board[row]: return False
    if num in board[:, col]: return False
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    if num in board[sr:sr+3, sc:sc+3]: return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
