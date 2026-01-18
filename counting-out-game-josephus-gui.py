import tkinter as tk
from tkinter import messagebox
import math


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            return
        # find the tail
        tail = self.head
        while tail.next != self.head:
            tail = tail.next
        tail.next = new_node
        new_node.next = self.head

    def tail(self):
        if not self.head:
            return None
        t = self.head
        while t.next != self.head:
            t = t.next
        return t

    def remove_after(self, prev):
        victim = prev.next
        if victim is self.head:
            if victim.next is victim:
                self.head = None
                return None
            self.head = victim.next
        prev.next = victim.next
        return prev.next


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Counting-Out Game")
        self.root.geometry("600x500")
        
        # game variables
        self.n = 0
        self.k = 0
        self.players = None
        self.current = None
        self.prev = None
        self.remaining = 0
        self.buttons = {}
        self.round_num = 0
        
        self.make_gui()
    
    def make_gui(self):
        # title
        tk.Label(self.root, text="Counting-Out Game", font=("Arial", 16)).pack(pady=10)
        
        # inputs
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="N:").grid(row=0, column=0)
        self.n_entry = tk.Entry(input_frame, width=5)
        self.n_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="K:").grid(row=0, column=2)
        self.k_entry = tk.Entry(input_frame, width=5)
        self.k_entry.grid(row=0, column=3, padx=5)
        
        self.start_btn = tk.Button(input_frame, text="Start", command=self.start_game)
        self.start_btn.grid(row=0, column=4, padx=10)
        
        # area for player buttons
        self.game_area = tk.Frame(self.root)
        self.game_area.pack(pady=10, expand=True, fill='both')
        
        # eliminate button (hidden at start)
        self.eliminate_btn = tk.Button(self.root, text="Eliminate", command=self.eliminate)
        # don't pack yet
        
        # text area for messages (at bottom)
        self.text = tk.Text(self.root, height=8)
        self.text.pack(pady=10, side='bottom', fill='x')
    
    def start_game(self):
        # check inputs
        try:
            n = int(self.n_entry.get())
            k = int(self.k_entry.get())
        except:
            messagebox.showerror("Error", "Please enter numbers")
            return
            
        if n <= 1 or n >= 12:
            messagebox.showerror("Error", "N must be between 2 and 11")
            return
            
        if k < 1:
            messagebox.showerror("Error", "K must be at least 1")
            return
        
        self.n = n
        self.k = k
        
        # make the circular list
        self.players = CircularLinkedList()
        for i in range(n):
            self.players.append(i)
        
        self.remaining = n
        self.prev = self.players.tail()
        self.current = self.players.head
        self.round_num = 0
        
        # clear old game and show new players
        self.clear_game()
        self.show_players()
        self.eliminate_btn.pack(pady=10)
        
        # update text
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"Game started. N={n} K={k}\n")
        self.text.insert(tk.END, f"Players: {list(range(n))}\n")
    
    def show_players(self):
        self.buttons = {}
        
        # put players in a circle - centered in the game area
        self.game_area.update()  # make sure we have the current size
        center_x = self.game_area.winfo_width() // 2
        center_y = self.game_area.winfo_height() // 2 - 20  # adjust for equal padding
        radius = 80
        
        for i in range(self.n):
            angle = 2 * math.pi * i / self.n
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            btn = tk.Button(self.game_area, text=str(i), width=3, height=2)
            btn.place(x=x-15, y=y-15)  # center the button on the position
            self.buttons[i] = btn
    
    def eliminate(self):
        if self.remaining <= 1:
            return
        
        # count k steps
        for _ in range(self.k - 1):
            self.prev = self.current
            self.current = self.current.next
        
        # remove this player
        eliminated = self.current.value
        self.current = self.players.remove_after(self.prev)
        self.remaining -= 1
        self.round_num += 1
        
        # remove button
        if eliminated in self.buttons:
            self.buttons[eliminated].destroy()
            del self.buttons[eliminated]
        
        # update text
        self.text.insert(tk.END, f"Round {self.round_num}: Player {eliminated} has been eliminated!\n")
        self.text.see(tk.END)
        
        # check if game over
        if self.remaining == 1:
            winner = self.current.value
            messagebox.showinfo("Game Over", f"Winner: Player {winner}")
            self.reset()
    
    def clear_game(self):
        for btn in self.buttons.values():
            btn.destroy()
        self.buttons = {}
    
    def reset(self):
        self.clear_game()
        self.eliminate_btn.pack_forget()
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, "Game over. Start a new game.\n")


# run the program
if __name__ == "__main__":
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()
