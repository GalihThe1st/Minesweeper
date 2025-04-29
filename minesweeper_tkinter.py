import random
import time
from tkinter import *

def minesweeper(game_diff):
    window = Tk()
    main_board = Frame(window)
    main_board.place(anchor="center", rely=0.4, relx=0.5)
    game_condition = [1]

    if game_diff == 0:
        col_length = 7
        row_length = 10
        mine_counter = 10
        window.geometry("400x400")
        window.title("Minesweeper (Easy)")
    elif (game_diff == 1):
        col_length = 15
        row_length = 20
        mine_counter = 40

        window.geometry("700x600")
        window.title("Minesweeper (Medium)")
    elif (game_diff == 2):
        col_length = 20
        row_length = 30
        mine_counter = 100

        window.geometry("1000x1000")
        window.title("Minesweeper (Hard)")

    back_board = [[] for row in range(col_length)]
    front_board = [[] for row in range(col_length)]

    def create_board():
        all_position = [(r,c) for r in range(row_length) for c in range(col_length)]
        mines_position = random.sample(all_position, mine_counter)

        for row in back_board:
            for tile in range(row_length):
                row.append("s")

        for (row, col) in mines_position:
            back_board[col][row] = "m"

        for row in back_board:
            for tile in row:
                print(tile, end=" ")
            print()
        print()

    create_board()

    def player_choose(row, col):
        if (game_condition[0] == 1):
            game_condition[0] = 0
            timer()
        
        adjacent_tiles = [(-1,-1), (0, -1), (1, -1),
                          (-1, 0),          (1,  0),
                          (-1, 1), (0,  1), (1,  1)] 
        
        def count_adjacent_mines(row_index, col_index):
            adjacent_mines = 0

            for neighbor in adjacent_tiles:
                if (((col_index + neighbor[1]) < 0) or ((row_index + neighbor[0]) < 0)):
                    continue

                try:
                    if (back_board[col_index + (neighbor[1])][row_index + (neighbor[0])] == "m"):
                        adjacent_mines += 1
                except IndexError:
                    continue

            return adjacent_mines
        
        def flood_fill(row_index, col_index):
            for neighbor in adjacent_tiles:
                new_col = col_index + neighbor[1]
                new_row = row_index + neighbor[0]

                if ((new_col < 0) or (new_row < 0)):
                    continue

                try:
                    if ((back_board[new_col][new_row] == "s") and (front_board[new_col][new_row].cget("state") == "normal")):
                        player_choose(new_row, new_col)
                except IndexError:
                    pass

        def winning_condition():
            unrevealed = 0

            for row in front_board:
                for tile in row:
                    if (tile.cget("state") == "normal") or (tile.cget("text") == "#"):
                        unrevealed += 1

            return (unrevealed == mine_counter)
        
        choosen = back_board[col][row]
        self = front_board[col][row]
        adjacent_mines = count_adjacent_mines(row, col)

        if (choosen == "m"):
            print("You've hit a mine")
            self.config(state="disabled", bg="red", fg="white", text="X")
            losing_text = Label(window, text="You've hit a mine! You lost! :(", font=("Times New Romans", 10))
            losing_text.place(anchor="center", relx=0.3, rely=0.8)
            restart_button = Button(window, text="Try Again?", font=("Times New Roman", 10), command= lambda: restart(window))
            restart_button.place(anchor="center", relx=0.5, rely=0.9)
            game_condition[0] = 1

            for col_index, row in enumerate(front_board):
                for row_index, tile in enumerate(row):
                    tile.config(state="disabled")
                    if (back_board[col_index][row_index] == "m"):
                        tile.config(bg="red")

        elif (choosen == "s"):
            game_condition[0] = 0
            if (adjacent_mines == 0):
                print("You didn't hit a mine")
                self.config(state="disabled", bg="cyan", fg="white", text=" ")
                print(self.cget("state"))
                game_condition[0] = 0
                flood_fill(row, col)
            else:
                self.config(state="disabled", bg="cyan", fg="white", text=adjacent_mines)
                print(self.cget("state"))
                game_condition[0] = 0

            if (winning_condition()):
                for col_index, row in enumerate(front_board):
                    for row_index, tile in enumerate(row):
                        if (back_board[col_index][row_index] == "m"):
                            tile.config(bg="yellow", fg="white", text="X", state="disabled")
                        elif (back_board[col_index][row_index] == "s"):
                            tile.config(bg="cyan")

                winning_text = Label(window, text="You win! :D", font=("Times New Romans", 10))
                winning_text.place(anchor="center", relx=0.3, rely=0.8)
                restart_button = Button(window, text="Play Again?", font=("Times New Roman", 10), command= lambda: restart(window))
                restart_button.place(anchor="center", relx=0.5, rely=0.9)
                game_condition[0] = 1

    def timer():
        second_count = [0]
        time_label = Label(window, text="00:00", font=("Times New Romans", 10))
        time_label.place(anchor="center", relx=0.8, rely=0.8)

        def time_count():
            second_count[0] += 1
            minutes = (second_count[0] // 60)
            seconds = (second_count[0] % 60)

            if (minutes < 10):
                minutes = (f"0{minutes}")
            if (seconds < 10):
                seconds = (f"0{seconds}")

            time_label.config(text=f"{minutes}:{seconds}")
            print(second_count)
            idk_lol()
        
        def idk_lol():
            if (game_condition[0] == 0):
                window.after(1000, time_count)
            elif (game_condition[0] == 1):
                return
            
        time_count()

    def flagging(row, col):
        self = front_board[col][row]
        if (self.cget("state") == "normal") and (self.cget("text") == ""):
            self.config(state="disabled", text="#")
            print("flagged")
        elif (self.cget("state") == "disabled") and (self.cget("text") == "#"):
            self.config(state="normal", text="")
            print("unflagged")

    def front_board_setting():
        for col_index, row in enumerate(front_board):
            for row_index in range(row_length):
                button = Button(main_board, height=1, width=2, command= lambda col=col_index, row=row_index: player_choose(row, col))
                button.bind("<Button-3>", lambda e, col=col_index, row=row_index: flagging(row, col))
                front_board[col_index].append(button)
                button.grid(column=row_index, row=col_index)

    front_board_setting()
    window.mainloop()

def restart(parent):
    parent.destroy()
    diff_interface()

def difficulty(diff,self ,parent):
    global game_diff
    self.config(state="disabled")
    parent.destroy()
    game_diff = diff
    minesweeper(game_diff)
    
# difficulty interface
def diff_interface():
    diff_window = Tk()
    diff_window.geometry("700x500")
    diff_window.title("Minesweeper")

    greeting_label = Label(text="Welcome to Minesweeper!", font=("Times New Roman", 20))
    greeting_label1 = Label(text="Choose the game's difficulty!", font=("Times New Roman", 10))

    greeting_label.place(anchor="center", relx=0.5, rely=0.25)
    greeting_label1.place(anchor="center", relx=0.5, rely=0.3)

    easy_button = Button(diff_window, height=5, width=20,text="Easy", bg="lime", fg="white" ,font=("Times New Roman", 10), command= lambda: difficulty(0, easy_button, diff_window))
    easy_button.place(anchor="center", relx=0.2, rely=0.55)

    medium_button = Button(diff_window, height=5, width=20, text="Medium",  bg="orange", fg="white" ,font=("Times New Roman", 10), command= lambda: difficulty(1,medium_button, diff_window))
    medium_button.place(relx=0.5, rely=0.55, anchor="center")

    hard_button = Button(diff_window, height=5, width=20, text="Hard",  bg="red", fg="white" ,font=("Times New Roman", 10), command= lambda: difficulty(2,hard_button, diff_window))
    hard_button.place(relx=0.8, rely=0.55, anchor="center")

    diff_window.mainloop()
diff_interface()
# difficulty interface
