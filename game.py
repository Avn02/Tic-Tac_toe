import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Tic Tac Toe - Play with Computer")
        self.root.configure(bg="#f0f8ff")
        self.player_symbol = 'X'
        self.computer_symbol = 'O'
        self.board = ['' for _ in range(9)]
        self.buttons = []
        self.game_over = False

        # Score tracking
        self.player_score = 0
        self.computer_score = 0
        self.draw_score = 0

        self.start_game()

    def start_game(self):
        self.create_widgets()

        # Let computer play first if it's 'X'
        if self.computer_symbol == 'X':
            self.root.after(400, self.computer_move)

    def create_widgets(self):
        tk.Label(self.root, text="Tic Tac Toe", font=("Comic Sans MS", 28, "bold"),
                 fg="#333", bg="#f0f8ff").pack()

        self.score_label = tk.Label(self.root, text=self.get_score_text(),
                                    font=("Arial", 14), bg="#f0f8ff")
        self.score_label.pack(pady=5)

        self.frame = tk.Frame(self.root, bg="#f0f8ff")
        self.frame.pack()

        for i in range(9):
            button = tk.Button(self.frame, text='', font=('Helvetica', 24, 'bold'),
                               width=5, height=2, bg="#ffffff", activebackground="#add8e6",
                               command=lambda i=i: self.player_move(i))
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

    def get_score_text(self):
        return f"🧍 You: {self.player_score}    💻 Computer: {self.computer_score}    🤝 Draws: {self.draw_score}"

    def player_move(self, index):
        if not self.board[index] and not self.game_over:
            self.board[index] = self.player_symbol
            self.buttons[index].config(text=self.player_symbol, fg='blue', state='disabled', bg="#e0f7ff")
            winner = self.check_winner(self.board)
            if winner:
                self.end_game("🎉 You Win!", winner)
                return
            elif '' not in self.board:
                self.end_game("🤝 It's a Draw!", None)
                return
            self.root.after(400, self.computer_move)

    def computer_move(self):
        if self.game_over:
            return

        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = self.computer_symbol
                score = self.minimax(self.board, 0, False)
                self.board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.board[best_move] = self.computer_symbol
            self.buttons[best_move].config(text=self.computer_symbol, fg='red', state='disabled', bg="#ffe0e0")

        winner = self.check_winner(self.board)
        if winner:
            self.end_game("😞 Computer Wins!", winner)
        elif '' not in self.board:
            self.end_game("🤝 It's a Draw!", None)

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner(board)
        if winner == self.computer_symbol:
            return 1
        elif winner == self.player_symbol:
            return -1
        elif '' not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = self.computer_symbol
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = self.player_symbol
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, board):
        win_combos = [(0,1,2),(3,4,5),(6,7,8),
                      (0,3,6),(1,4,7),(2,5,8),
                      (0,4,8),(2,4,6)]
        for a,b,c in win_combos:
            if board[a] and board[a] == board[b] == board[c]:
                self.winning_combo = (a, b, c)
                return board[a]
        return None

    def end_game(self, result, winner_symbol):
        self.game_over = True
        if winner_symbol == self.player_symbol:
            self.player_score += 1
        elif winner_symbol == self.computer_symbol:
            self.computer_score += 1
        else:
            self.draw_score += 1

        messagebox.showinfo("Game Over", result)
        self.score_label.config(text=self.get_score_text())
        self.add_reset_button()

    def add_reset_button(self):
        self.reset_btn = tk.Button(self.root, text="🔁 Play Again", font=("Arial", 14, "bold"),
                                   bg="#4CAF50", fg="white", activebackground="#45a049",
                                   padx=10, pady=5, command=self.reset_game)
        self.reset_btn.pack(pady=15)

    def reset_game(self):
        self.board = ['' for _ in range(9)]
        for button in self.buttons:
            button.config(text='', state='normal', bg='white')
        self.game_over = False
        if hasattr(self, 'reset_btn'):
            self.reset_btn.destroy()
        if hasattr(self, 'winning_combo'):
            del self.winning_combo

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    TicTacToe(root)
    root.mainloop()
