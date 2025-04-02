import tkinter as tk
from tkinter import ttk
from config import config
import os

class ConfigGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Config")

        # Set the window icon
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/Misc/logo.png")
            self.root.iconbitmap(logo_path)
        except Exception as e:
            print(f"Error loading logo: {e}")

        self.board_var = tk.StringVar(value=config.board)
        self.piece_var = tk.StringVar(value=config.pieces)
        self.difficulty_var = tk.StringVar(value=config.difficulty)
        self.console_var = tk.BooleanVar(value=config.show_console)
        self.create_header()
        self.create_board_menu()
        self.create_piece_menu()
        self.create_difficulty_menu()
        self.create_console_option()
        self.create_buttons()
        self.root.mainloop()

    def create_header(self):
        label = tk.Label(self.root, text="Games Config", font=("Arial", 24), pady=10)
        label.pack()

    def create_board_menu(self):
        menu_frame = ttk.LabelFrame(self.root, text="Boards", padding=(10, 10))
        menu_frame.pack(padx=5, pady=5, fill=tk.X)
        dd1 = tk.OptionMenu(menu_frame, self.board_var, "Brown", "Green", "Blue")
        dd1.pack(fill=tk.X)

    def create_piece_menu(self):
        menu_frame = ttk.LabelFrame(self.root, text="Pieces", padding=(10, 10))
        menu_frame.pack(padx=5, pady=5, fill=tk.X)
        dd2 = tk.OptionMenu(menu_frame, self.piece_var, "Neo", "Bases", "Glass")
        dd2.pack(fill=tk.X)

    def create_difficulty_menu(self):
        menu_frame = ttk.LabelFrame(self.root, text="Difficulty", padding=(10, 10))
        menu_frame.pack(padx=5, pady=5, fill=tk.X)
        dd3 = tk.OptionMenu(menu_frame, self.difficulty_var, "Easy", "Medium", "Hard")
        dd3.pack(fill=tk.X)

    def create_console_option(self):
        console_frame = ttk.LabelFrame(self.root, text="Console", padding=(10, 10))
        console_frame.pack(padx=5, pady=5, fill=tk.X)
        cb = tk.Checkbutton(console_frame, text="Show Console", variable=self.console_var)
        cb.pack()

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=10, side=tk.BOTTOM, anchor=tk.W)
        save_button = tk.Button(button_frame, text="Save & Start", command=self.save_and_close)
        save_button.pack(side=tk.LEFT, padx=5)
        quit_button = tk.Button(button_frame, text="Quit", command=self.root.destroy)
        quit_button.pack(side=tk.LEFT)

    def save_and_close(self):
        config.board = self.board_var.get()
        config.pieces = self.piece_var.get()
        config.difficulty = self.difficulty_var.get()
        config.show_console = self.console_var.get()
        self.root.destroy()

if __name__ == "__main__":
    ConfigGUI()