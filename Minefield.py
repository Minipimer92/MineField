import tkinter as tk
import random

class MineField:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = []
        self.create_grid()
        self.bandierina = tk.PhotoImage(file='assets/bandierina.png')
        self.cool= tk.PhotoImage(file='assets/smiley_cool.png')
        self.smile= tk.PhotoImage(file='assets/smiley.png')
        self.dead= tk.PhotoImage(file='assets/smiley_rip.png')
        self.reset_button = tk.Button(master, image=self.smile, command=self.reset_game)
        self.reset_button.grid(row=rows, column=0, columnspan=cols, pady=5)

    def create_grid(self, ):
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                btn = tk.Button(self.master, width=2, height=1, bg = "light gray", command=lambda r=r, c=c: self.check_cell(r, c))
                btn.grid(row=r, column=c)
                row.append(btn)
                btn.bind("<Button-3>", lambda event, r=r, c=c: self.mark_cell(event, r, c))
            self.grid.append(row)

        # Place mines randomly
        self.mines_coords = []
        for _ in range(self.mines):
            row = random.randint(0, self.rows-1)
            col = random.randint(0, self.cols-1)
            self.grid[row][col]["text"] = "X"
            self.grid[row][col]["fg"] = "light gray"
            self.mines_coords.append((row,col))
        self.calculate_numbers()

    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c]["text"] != "X":
                    count = 0
                    for row in range(r-1, r+2):
                        for col in range(c-1, c+2):
                            if (row >= 0 and row < self.rows) and (col >= 0 and col < self.cols):
                                if self.grid[row][col]["text"] == "X":
                                    count += 1
                    self.grid[r][c]["text"] = count if count > 0 else ""
                    self.grid[r][c]["fg"] = "light gray"
                    
    def check_cell(self, row, col):
        if self.grid[row][col]["text"] == "X":
            self.game_over()
        else:
            self.grid[row][col]["fg"] = "black"
            self.grid[row][col]["bg"] = "white"
            self.grid[row][col]["state"] = "disabled"
            if self.grid[row][col]["text"] == "":
                self.check_neighbors(row, col)
        self.check_victory()

    def check_neighbors(self, row, col):
        for r in range(row-1,row+2):
            for c in range(col-1,col+2):
                if r>=0 and r<self.rows and c>=0 and c and c<self.cols and self.grid[r][c]["state"] != "disabled":
                    if self.grid[r][c]["text"] != "X":
                        self.grid[r][c]["fg"] = "black"
                        self.grid[r][c]["bg"] = "white"
                        self.grid[r][c]["state"] = "disabled"
                    if self.grid[r][c]["text"] == "":
                        self.check_neighbors(r,c)
                    self.check_victory()

    def mark_cell(self,event,row,col):
        if self.grid[row][col]["state"] != "disabled":
            if self.grid[row][col]["text"] != "!":
                self.grid[row][col]["text"] = "!"
                self.grid[row][col]["state"] = "disabled"
                self.grid[row][col].bind("<Button-3>", lambda event, r=row, c=col: self.remove_mark(event, r, c))
            else:
                self.remove_mark(event,row,col)
                self.check_victory()

    def remove_mark(self,event,row,col):
        self.grid[row][col]["text"] = ""
        self.grid[row][col]["state"] = "normal"
        self.grid[row][col].bind("<Button-3>", lambda event, r=row, c=col: self.mark_cell(event, r, c))

    def game_over(self):
        for row in self.grid:
            for btn in row:
                btn["state"] = "disabled"
                btn["fg"] = "black"
        for coord in self.mines_coords:
            self.grid[coord[0]][coord[1]]["fg"] = "red"
        self.master.config(bg="red")        
        self.reset_button.configure(image=self.dead)

    def check_victory(self):
        if all( [self.grid[r][c]["state"]=="disabled" for r in range(self.rows) for c in range(self.cols)] ):
            for coord in self.mines_coords:
                if self.grid[coord[0]][coord[1]]["text"] != "!":
                    self.game_over()
                    return
            self.victory()

    def victory(self):
        self.master.config(bg="green")
        for row in self.grid:
            for btn in row:
                btn["state"] = "disabled"
        self.reset_button.configure(image=self.cool)
        
    def reset_game(self):
        for row in self.grid:
            for col in row:
                for btn in row:
                    btn["text"] = ""
                    btn["fg"] = "black"
                    btn["state"] = "normal"
                    btn.bind("<Button-3>", lambda event, r=row, c=col: self.mark_cell(event, r, c))
        self.master.config(bg="SystemButtonFace")
        self.reset_button.configure(image=self.smile)
        self.grid = []
        self.create_grid()

root = tk.Tk()
root.title("Minesweeper")
root.resizable(False, False)
mine_field = MineField(root, 10, 10, 10)
root.iconbitmap("assets/mina.ico")
root.mainloop()
