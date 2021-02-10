import tkinter
from tkinter import messagebox as msgbox
from PIL import Image, ImageDraw, ImageTk
from functools import partial
from random import choice
import sys

FONT = "Malgun Gothic"
FONT_SIZE = 18
PADX_VALUE = 30

class game(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.title("Play Tic Tac Toe with AI")

        self.score = {"AI":0, "Human":0, "Tie":0}
        # --------------------------------------
        self.game_frame = tkinter.Frame(self)
        self.game_frame.grid(row=0, column=0)

        self.scoreFrame = tkinter.Frame(self)
        self.scoreFrame.grid(row=1, column=0)

        self.scoreLabelAI = tkinter.Label(self.scoreFrame, text=f"AI:{self.score['AI']}", font=(FONT, FONT_SIZE))
        self.scoreLabelAI.grid(row=0, column=0, padx=PADX_VALUE)
        
        self.scoreLabelHuman = tkinter.Label(self.scoreFrame, text=f"Human:{self.score['Human']}", font=(FONT, FONT_SIZE))
        self.scoreLabelHuman.grid(row=0, column=1, padx=PADX_VALUE)
        
        self.scoreLabelTie = tkinter.Label(self.scoreFrame, text=f"Tie:{self.score['Tie']}", font=(FONT, FONT_SIZE))
        self.scoreLabelTie.grid(row=0, column=2, padx=PADX_VALUE)
        
        self.board = [" " for i in range(9)]

        self.images = {
            "X": self.xShape("white"),
            "O": self.oShape("white"),
            "X-winner": self.xShape("green"),
            "O-winner": self.oShape("green"),
            "plain": self.plainArea()
        }

        self.tiles = dict()
        for i in range(9):
            tile = {
                "id": i,
                "Button": tkinter.Button(self.game_frame, image=self.images["plain"], disabledforeground="white", command=partial(self.onClick, i))
            }
            #Row and column
            r, c = divmod(i, 3)

            # tile["Button"].bind(BTN_CLICK, self.onClickWrapper(i))
            tile["Button"].grid(row=r, column=c, sticky = "NWSE")

            self.tiles[i] = tile

    def xShape(self, color):
        width, height = 150, 150
        new = Image.new("RGB", (width, height), color)
        shape = ImageDraw.Draw(new)
        linePoints = [(30,30), (30, 120), (120, 30), (120, 120)]
        shape.line([linePoints[0], linePoints[3]],fill="black", width=6)
        shape.line([linePoints[1], linePoints[2]],fill="black", width=6)
        return ImageTk.PhotoImage(new)

    def oShape(self, color):
        width, height = 150, 150
        new = Image.new("RGB", (width, height), color)
        shape = ImageDraw.Draw(new)
        shape.ellipse([30, 30, 120, 120], outline="black", width=6)
        return ImageTk.PhotoImage(new)

    def plainArea(self):
        width, height = 150, 150
        white = (255, 255, 255)
        new = Image.new("RGB", (width, height), white)
        return ImageTk.PhotoImage(new)

    def updateScore(self, result):
        if result == "Human":
            self.score["Human"] += 1
            self.scoreLabelHuman["text"] = f"Human:{self.score['Human']}"

        elif result == "AI":
            self.score["AI"] += 1
            self.scoreLabelAI["text"] = f"AI:{self.score['AI']}"

        elif result == "Tie":
            self.score["Tie"] += 1
            self.scoreLabelTie["text"] = f"Tie:{self.score['Tie']}"

        else:
            raise ValueError("Invalid value")

    def onClick(self, number):
        if not self.board[number] == " ":
            return
        self.makeMove(number, "X")
        
        move = self.AImove()

        self.makeMove(move, "O")

    def makeMove(self, move, player):
        self.tiles[move]["Button"].config(image=self.images[player])
        self.board[move] = player
        self.check()

    def AImove(self):
        bestVal = float("-inf")
        bestMove = -1
        tempBoard = self.board
        
        for i in self.listPossibleMoves(tempBoard):
            tempBoard[i] = "O"

            moveValue = self.AIminimax(tempBoard, False)

            tempBoard[i] = " "
            
            if (moveValue > bestVal):
                
                bestMove = i
                bestVal = moveValue

    
        return bestMove

    def AIminimax(self, board, isMaximixing):
                
        score = self.AIevaluate(board)
        
        if score == 1:
            return score

        elif score == -1:
            return score

        elif not self.AIisMovesLeft(board):
            return 0
        
        if (isMaximixing):
            
            best = float("-inf")

            for i in self.listPossibleMoves(board):
                board[i] = "O"

                best = max(best, self.AIminimax(board, not isMaximixing))

                board[i] = " "
            
            return best

        else:
            best = float("inf")
            
            for i in self.listPossibleMoves(board):

                board[i] = "X"

                best = min(best, self.AIminimax(board, not isMaximixing))

                board[i] = " "
            
            return best

    def AIcalculate(self, board):
        
        for i in range(0, 9, 3):
            if self.isSame(board[i], board[i+1], board[i+2]):
                return board[i]

        for i in range(3):
            if self.isSame(board[i], board[i+3], board[i+6]):
                return board[i]

        if self.isSame(board[0], board[4], board[8]):
            return board[4]

        elif self.isSame(board[2], board[4], board[6]):
            return board[4]

        else:
            return False

    def AIevaluate(self, board):
        result = self.AIcalculate(board)
        
        if result == "X":
            return -1

        elif result == "O":
            return 1

        else:
            return 0

    def AIisMovesLeft(self, board):
        return False if len(self.listPossibleMoves(board))==0 else True

    def listPossibleMoves(self, board):
        return [i for i in range(9) if board[i]==" "]
        
    def gameOver(self, result):
        if self.ask(result):
            self.clear()

        else:
            sys.exit()

    def isSame(self, a, b, c):
        return a == b == c and not a == " "

    def makeGreen(self, a, b, c):
        self.tiles[a]["Button"].config(image=self.images[f"{self.board[a]}-winner"])
        self.tiles[b]["Button"].config(image=self.images[f"{self.board[b]}-winner"])
        self.tiles[c]["Button"].config(image=self.images[f"{self.board[c]}-winner"])

    def check(self):
        result = self.checkInner()

        if (not result) and not (" " in self.board):
            self.updateScore("Tie")
            self.gameOver("Tie")

        elif result == "X":
            self.updateScore("Human")
            self.gameOver(result)

        elif result == "O":
            self.updateScore("AI")
            self.gameOver(result)

    def checkInner(self):
        
        for i in range(0, 9, 3):
            if self.isSame(self.board[i], self.board[i+1], self.board[i+2]):
                self.makeGreen(i, i+1, i+2)
                return self.board[i]

        for i in range(3):
            if self.isSame(self.board[i], self.board[i+3], self.board[i+6]):
                self.makeGreen(i, i+3, i+6)
                return self.board[i]

        if self.isSame(self.board[0], self.board[4], self.board[8]):
            self.makeGreen(0, 4, 8)
            return self.board[4]

        elif self.isSame(self.board[2], self.board[4], self.board[6]):
            self.makeGreen(2, 4, 6)
            return self.board[4]

        else:
            return False

    def ask(self, status):
        msg = ""
        if status == "X":
            msg = "You Win! Play again?"

        elif status == "O":
            msg = "You lose! Play again?"

        elif status == "Tie":
            msg = "Tie, Play Again?"

        return msgbox.askyesno("Game Over", msg)

    def clear(self):
        for i in range(9):
            self.tiles[i]["Button"].config(image=self.images["plain"])
        self.board = [" " for i in range(9)]
        

if __name__ == "__main__":
    
    myGame = game()
    
    myGame.mainloop()