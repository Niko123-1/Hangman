from tkinter import Tk
import Hangman as hg



if __name__ == "__main__":
    root = Tk()
    game = hg.HangmanGame(root)
    root.mainloop()