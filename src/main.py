import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QGridLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import chess
import chess.engine
from config import config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.setGeometry(700, 300, 800, 800)
        self.setWindowTitle("Chess")

        # Set the window icon
        try:
            logo_path = os.path.join(self.base_dir, "assets/Misc/logo.png")
            self.setWindowIcon(QIcon(logo_path))
        except Exception as e:
            print(f"Error loading logo: {e}")

        self.init_ui()
        self.selected_square = None

    def init_ui(self):
        self.board_label = QLabel(self)
        self.board_label.setGeometry(0, 0, 800, 800)
        board_path = os.path.join(self.base_dir, f"assets/Boards/{config.board}.png")
        self.board_pixmap = QPixmap(board_path)
        if self.board_pixmap.isNull():
            raise FileNotFoundError(f"Could not load board image from {board_path}")
        self.board_label.setPixmap(self.board_pixmap)
        self.board_label.setScaledContents(True)
        self.board_label.lower()
        self.button_grid = QGridLayout()
        self.button_grid.setSpacing(0)
        self.button_grid.setContentsMargins(0, 0, 0, 0)
        self.buttons = []
        for i in range(8):
            for j in range(8):
                button = QPushButton(self)
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda checked, row=i, col=j: self.on_button_click(row, col))
                self.buttons.append(button)
                self.button_grid.addWidget(button, i, j)
        central_widget = QWidget(self)
        central_widget.setLayout(self.button_grid)
        self.setCentralWidget(central_widget)
        self.init_chess_board()

    def init_chess_board(self):
        self.board = chess.Board()
        difficulty_map = {"Easy": 1, "Medium": 5, "Hard": 10}
        difficulty_level = difficulty_map.get(config.difficulty, 5)
        stockfish_path = os.path.join(self.base_dir, "stockfish/stockfish-windows-x86-64-avx2.exe")
        if not os.path.isfile(stockfish_path):
            print(f"Stockfish binary not found at: {stockfish_path}")
            sys.exit(1)
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            self.engine.configure({"Skill Level": difficulty_level})
        except Exception as e:
            print(f"Error initializing Stockfish: {e}")
            sys.exit(1)
        self.update_board()

    def update_board(self):
        for i in range(8):
            for j in range(8):
                piece = self.board.piece_at(chess.square(j, 7 - i))
                button = self.buttons[i * 8 + j]
                if piece:
                    color_code = "w" if piece.color else "b"
                    piece_type_code = chess.piece_symbol(piece.piece_type)
                    piece_image = QPixmap(os.path.join(self.base_dir, f"assets/Pieces/{config.pieces}/{color_code}{piece_type_code}.png"))
                    if piece_image.isNull():
                        print(f"Error loading piece image: {color_code}{piece_type_code}.png")
                        return
                    icon_size = button.size()
                    button.setIcon(QIcon(piece_image))
                    button.setIconSize(icon_size)
                    button.setStyleSheet("background: transparent;")
                else:
                    button.setIcon(QIcon())
                    button.setStyleSheet("background: transparent;")
        self.check_game_status()

    def check_game_status(self):
        if self.board.is_checkmate():
            self.show_message("Checkmate!", "The game is over. Checkmate!")
            self.board.reset()
            self.update_board()
        elif self.board.is_stalemate():
            self.show_message("Stalemate!", "The game is over. Stalemate!")
            self.board.reset()
            self.update_board()
        elif self.board.is_insufficient_material():
            self.show_message("Draw!", "The game is over. Insufficient material!")
            self.board.reset()
            self.update_board()
        elif self.board.can_claim_fifty_moves():
            self.show_message("Draw!", "The game is over. Fifty-move rule!")
            self.board.reset()
            self.update_board()
        elif self.board.can_claim_threefold_repetition():
            self.show_message("Draw!", "The game is over. Threefold repetition!")
            self.board.reset()
            self.update_board()

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def on_button_click(self, row, col):
        selected_square = chess.square(col, 7 - row)
        if self.selected_square is None:
            piece = self.board.piece_at(selected_square)
            if piece and piece.color == self.board.turn:
                self.selected_square = selected_square
        else:
            move = chess.Move(self.selected_square, selected_square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()
                self.selected_square = None
                self.make_engine_move()
            else:
                print("Invalid move.")
                self.selected_square = None

    def make_engine_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=1.0))
        if config.show_console:
            info = self.engine.analyse(self.board, chess.engine.Limit(time=1.0))
            print(f"Stockfish evaluation: {info['score']}")
        self.board.push(result.move)
        self.update_board()

def main():
    app = QApplication(sys.argv)
    from configGUI import ConfigGUI
    ConfigGUI()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()