import tkinter as tk
from tkinter import messagebox

class ChopsticksGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("割り箸ゲーム")
        self.geometry("400x200")

        self.player1_hands = [1, 1]
        self.player2_hands = [1, 1]
        self.current_player = 1

        self.init_ui()

    def init_ui(self):
        self.player1_label = tk.Label(self, text="プレイヤー1")
        self.player1_label.grid(row=0, column=0)

        self.player2_label = tk.Label(self, text="プレイヤー2")
        self.player2_label.grid(row=0, column=3)

        self.player1_hand1_label = tk.Label(self, text=str(self.player1_hands[0]))
        self.player1_hand1_label.grid(row=1, column=0)

        self.player1_hand2_label = tk.Label(self, text=str(self.player1_hands[1]))
        self.player1_hand2_label.grid(row=2, column=0)

        self.player2_hand1_label = tk.Label(self, text=str(self.player2_hands[0]))
        self.player2_hand1_label.grid(row=1, column=3)

        self.player2_hand2_label = tk.Label(self, text=str(self.player2_hands[1]))
        self.player2_hand2_label.grid(row=2, column=3)

        self.attack_button = tk.Button(self, text="攻撃", command=self.attack)
        self.attack_button.grid(row=3, column=0, padx=10)

        self.split_button = tk.Button(self, text="分割", command=self.split)
        self.split_button.grid(row=3, column=1, padx=10)

    def update_labels(self):
        self.player1_hand1_label.configure(text=str(self.player1_hands[0]))
        self.player1_hand2_label.configure(text=str(self.player1_hands[1]))
        self.player2_hand1_label.configure(text=str(self.player2_hands[0]))
        self.player2_hand2_label.configure(text=str(self.player2_hands[1]))

    def change_player(self):
        self.current_player = 3 - self.current_player

    def is_alive(self, hand):
        return 1 <= hand <= 4

    def attack(self):
        if self.current_player == 1:
            attacker_hands = self.player1_hands
            defender_hands = self.player2_hands
        else:
            attacker_hands = self.player2_hands
            defender_hands = self.player1_hands

        attack_hand = tk.simpledialog.askinteger("攻撃手", "攻撃する手を選択してください (1 or 2)")
        if not self.is_alive(attacker_hands[attack_hand - 1]):
            messagebox.showerror("エラー", "選択された手は生きていません。")
            return
        defend_hand = tk.simpledialog.askinteger("防御手", "防御する手を選択してください (1 or 2)")
        if not self.is_alive(defender_hands[defend_hand - 1]):
            messagebox.showerror("エラー", "選択された手は生きていません。")
            return
        defender_hands[defend_hand - 1] += attacker_hands[attack_hand - 1]

        if defender_hands[defend_hand - 1] >= 5:
            defender_hands[defend_hand - 1] %= 5

        self.update_labels()
        self.check_winner()
        self.change_player()

    def split(self):
        if self.current_player == 1:
            player_hands = self.player1_hands
        else:
            player_hands = self.player2_hands

        if not self.is_alive(player_hands[0]) or not self.is_alive(player_hands[1]):
            messagebox.showerror("エラー", "両手が生きている場合のみ分割が可能です。")
            return

        new_hand1 = tk.simpledialog.askinteger("新しい手1", "新しい手1の指の本数を入力してください。")
        new_hand2 = player_hands[0] + player_hands[1] - new_hand1

        if new_hand1 == player_hands[0] or new_hand1 == player_hands[1] or new_hand1 < 0 or new_hand2 < 0:
            messagebox.showerror("エラー", "不正な指の本数です。")
            return

        player_hands[0] = new_hand1
        player_hands[1] = new_hand2

        self.update_labels()
        self.change_player()

    def check_winner(self):
        if not self.is_alive(self.player1_hands[0]) and not self.is_alive(self.player1_hands[1]):
            messagebox.showinfo("勝者", "プレイヤー2が勝ちました！")
            self.destroy()
        elif not self.is_alive(self.player2_hands[0]) and not self.is_alive(self.player2_hands[1]):
            messagebox.showinfo("勝者", "プレイヤー1が勝ちました！")
            self.destroy()

if __name__ == "__main__":
    game = ChopsticksGame()
    game.mainloop()