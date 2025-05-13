import random
from tkinter import *

def restart(parent):
    parent.destroy()
    diff_interface()

class Minesweeper:
    def __init__(self, difficulty):
        self.main_window = Tk()
        self.main_board = Frame(self.main_window)
        self.main_board.place(anchor="center", relx=0.5, rely=0.4)
        self.game_flow = False
        self.all_tiles = []

        if difficulty == 0:
            self.col = 7
            self.row = 10
            self.mines = 10
            self.main_window.geometry("400x400")
            self.main_window.title("Minesweeper (Easy)")
        elif difficulty == 1:
            self.col = 15
            self.row = 20
            self.mines = 40
            self.main_window.geometry("700x600")
            self.main_window.title("Minesweeper (Medium)")
        elif difficulty == 2:
            self.col = 20
            self.row = 30
            self.mines = 100
            self.main_window.geometry("1000x1000")
            self.main_window.title("Minesweeper (Hard)")

        mine_position = random.sample(range(self.col * self.row), self.mines)

        for col in range(self.col):
            for row in range(self.row):
                index = (col * self.row) + row
                is_mine = index in mine_position
                self.Tile(col, row, is_mine, self)

        self.main_board.mainloop()

    def timer(self):
        second_counter = [0]
        time_label = Label(self.main_window, text="00:00", font=("Times New Romans", 10))
        time_label.place(anchor="center", relx=0.8, rely=0.8)

        def time_count():
            second_counter[0] += 1
            minutes = (second_counter[0] // 60)
            seconds = (second_counter[0] % 60)

            if (minutes < 10):
                minutes = (f'0{minutes}')
            if (seconds < 10):
                seconds = (f'0{seconds}')

            time_label.config(text=f"{minutes}:{seconds}")
            observer()

        def observer():
            if (self.game_flow == True):
                self.main_window.after(1000, time_count)
            else:
                return
        
        observer()

    class Tile:
        def __init__(self, row_index, col_index ,back_value, parent): 
            self.parent = parent # will pass the Minesweeper object here
            self.row_index = row_index
            self.col_index = col_index
            self.is_mine = back_value
            self.is_revealed = False
            self.is_flagged = False
            self.adjacent_mines = 0

            self.button = Button(
                self.parent.main_board,
                height = 1,
                width = 2,
                command= self.reveal
            )
            self.button.bind("<Button-3>", self.flagging)

            self.parent.all_tiles.append(self)
            self.button.grid(row=self.row_index, column=self.col_index)

        def reveal(self):

            adjacent_tiles = [(-1,-1), (0,-1), (1,-1),
                              (-1, 0),         (1, 0),
                              (-1, 1), (0, 1), (1, 1)]
            
            def count_adjacent_mines():
                adjacent_mines = 0

                for neighbor in adjacent_tiles:
                    for tile in self.parent.all_tiles:
                        if (tile.row_index == (self.row_index + neighbor[0])) and (tile.col_index == (self.col_index + neighbor[1])):
                            if (tile.is_mine):
                                adjacent_mines += 1

                return adjacent_mines

            def flood_fill():
                for neighbor in adjacent_tiles:
                    new_tile = None 
                    new_row = self.row_index + neighbor[0]
                    new_col = self.col_index + neighbor[1]
                
                    for tile in self.parent.all_tiles:
                        if (tile.row_index == new_row) and (tile.col_index == new_col):
                            new_tile = tile

                    if (new_tile and not new_tile.is_mine and not new_tile.is_revealed):
                        new_tile.reveal()

            def winning_condition():
                unrevealed = 0

                for tile in self.parent.all_tiles:
                    if (tile.is_revealed == False):
                        unrevealed += 1

                return self.parent.mines == unrevealed
            
            if (self.parent.game_flow == False):
                if (self.is_mine):
                    self.is_mine = False
                
                    def replacememt():
                        replacement_tiles = random.choice(self.parent.all_tiles)
                        if (replacement_tiles.is_mine):
                            return replacememt()
                        else:
                            return replacement_tiles
                        
                    replacement = replacememt()
                    replacement.is_mine = True

                self.parent.game_flow = True

                for neighbor in adjacent_tiles:
                    for tile in self.parent.all_tiles:
                        if (tile.row_index == (self.row_index + neighbor[0])) and (tile.col_index == (self.col_index + neighbor[1])) and (not tile.is_mine):
                            tile.reveal()
                        
                self.parent.timer()

            if (self.is_mine):
                self.parent.game_flow = False
                losing_text = Label(self.parent.main_window, text="You've hit a mine! You lost! :(", font=("Times New Romans", 10))
                losing_text.place(anchor="center", relx=0.3, rely=0.8)
                restart_button = Button(self.parent.main_window, text="Try Again?", font=("Times New Roman", 10), command= lambda: restart(self.parent.main_window))
                restart_button.place(anchor="center", relx=0.5, rely=0.9)
                for tile in self.parent.all_tiles:
                    tile.is_revealed = True
                    tile.button.config(state="disabled")

                    if (tile.is_mine):
                        tile.button.config(bg = "red", text="X")

            elif (not self.is_mine):
                mine_counter = count_adjacent_mines()
                if (mine_counter == 0):
                    self.is_revealed = True
                    self.button.config(state="disabled", bg="cyan", text="")
                    flood_fill()
                else:
                    self.is_revealed = True
                    self.button.config(state="disabled", bg="cyan", text=mine_counter)

                if (winning_condition()):
                    self.parent.game_flow = False
                    for tile in self.parent.all_tiles:
                        if (tile.is_mine):
                            tile.is_revealed = True
                            tile.button.config(state="disabled", bg="yellow", text="X")
                        else:
                            tile.is_revealed = True
                            tile.button.config(state="disabled", bg="cyan")

                    winning_text = Label(self.parent.main_window, text="You win! :D", font=("Times New Romans", 10))
                    winning_text.place(anchor="center", relx=0.3, rely=0.8)
                    restart_button = Button(self.parent.main_window, text="Play Again?", font=("Times New Roman", 10), command= lambda: restart(self.parent.main_window))
                    restart_button.place(anchor="center", relx=0.5, rely=0.9)

        def flagging(self, event):
            if (self.is_revealed):
                return
            
            if (self.is_flagged):
                self.is_flagged = False
                self.button.config(state="normal", text="")
            else:
                self.is_flagged = True
                self.button.config(state="disabled", text="X")
                

def difficulty(diff, parent):
    if diff == 0:
        parent.destroy()
        game = Minesweeper(0)
    elif diff == 1:
        parent.destroy()
        game = Minesweeper(1)
    elif diff == 2:
        parent.destroy()
        game = Minesweeper(2)

def diff_interface():
    diff_window = Tk()
    diff_window.geometry("700x500")
    diff_window.title("Minesweeper")

    greeting_label = Label(text="Welcome to Minesweeper!", font=("Times New Roman", 20))
    greeting_label1 = Label(text="Choose the game's difficulty!", font=("Times New Roman", 10))

    greeting_label.place(anchor="center", relx=0.5, rely=0.25)
    greeting_label1.place(anchor="center", relx=0.5, rely=0.3)

    easy_button = Button(diff_window, height=5, width=20,text="Easy", bg="lime", fg="white" ,font=("Times New Roman", 10), command= lambda: difficulty(0, diff_window))
    easy_button.place(anchor="center", relx=0.2, rely=0.55)

    medium_button = Button(diff_window, height=5, width=20, text="Medium",  bg="orange", fg="white" ,font=("Times New Roman", 10), command= lambda: difficulty(1, diff_window))
    medium_button.place(relx=0.5, rely=0.55, anchor="center")

    hard_button = Button(diff_window, height=5, width=20, text="Hard",  bg="red", fg="white" ,font=("Times New Roman", 10), command= lambda: difficulty(2, diff_window))
    hard_button.place(relx=0.8, rely=0.55, anchor="center")

    diff_window.mainloop()
diff_interface()

