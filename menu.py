"""
A module for the menu screen
"""
import tkinter as tk
import game

firstkey = False
secondkey = False
thirdkey = False
invalidKeys = True

class Menu():
    """
    Class which contains all the elements needed for the menu
    """
    def __init__(self):
        """
        Initiliase menu variables
        """
        self.menu = tk.Tk()
        self.switch = False
        self.userset = False
        self.keys = "Arrow"
    
    def setWindow(self, height, width):
        """
        Set dimensions of menu and create all buttons needed. If the save file is empty, the load button is greyed out.
        """
        self.menu.geometry("{height}x{width}".format(height = height, width = width))
        self.menu.resizable(height = False, width = False)
        self.menu.title("Menu")
        self.image = tk.PhotoImage(file="level.png")
        
        self.backgroundOne = canvas.create_image(1366/2, 768/2, image = self.image, anchor=tk.CENTER)
        self.backgroundTwo = canvas.create_image(2000, 768/2, image = self.image, anchor=tk.CENTER)
        self.backgroundThree = canvas.create_image(3250, 768/2, image = self.image, anchor=tk.CENTER)

        self.entry = tk.Entry(canvas)
        self.userinput = canvas.create_window(700, 160, window = self.entry)
        self.startButton = tk.Button(canvas, text= "Start Game", command=self.startGame, height=3, width=40)
        self.loadButton = tk.Button(canvas, text= "Load Game", command=self.loadGame, height=3, width=40)
        self.wasdButton = tk.Button(canvas, text= "Use WASD", command=self.useWASD, height=3, width=40)
        self.arrowButton = tk.Button(canvas, text= "Use Arrows", command=self.useArrow, height=3, width=40)

        if saveFile == 0:
            self.loadButton['state'] = tk.DISABLED
        else:
            self.loadButton['state'] = tk.NORMAL
        canvas.create_window(700, 260, window=self.startButton)
        canvas.create_window(700, 350, window=self.loadButton)
        canvas.create_window(700, 530, window=self.wasdButton)
        canvas.create_window(700, 440, window=self.arrowButton)

    
    def startGame(self):
        """
        Calls the startGame functions from game.py with load set to false. If the start button is clicked
        """
        userInput = self.entry.get()
        if userInput != "":
            self.userset = True
        if self.userset:
            self.menu.destroy()
            game.startGame(False, userInput, self.keys)
            self.switch = True
    
    def loadGame(self):
        """
        Calls the startGame functions from game.py with load set to True. If the load button is clicked
        """
        userInput = self.entry.get()
        if userInput != "":
            self.userset = True
        if self.userset:
            self.menu.destroy()
            game.startGame(True, userInput, self.keys)
            self.switch = True
    
    def background(self):
        """
        Moves the background constantly while on the menu screen
        """
        while not self.switch:
            canvas.move(self.backgroundOne, -3, 0)
            canvas.move(self.backgroundTwo, -3, 0)
            canvas.move(self.backgroundThree, -3, 0)
            self.menu.after(20, self.menu.update())
            if canvas.coords(self.backgroundOne)[0] < -675:
                canvas.coords(self.backgroundOne, 3250, 768/2)
            elif canvas.coords(self.backgroundTwo)[0] < -675:
                canvas.coords(self.backgroundTwo, 3250, 768/2)
            elif canvas.coords(self.backgroundThree)[0] < -675:
                canvas.coords(self.backgroundThree, 3250, 768/2)
    
    def useWASD(self):
        """
        sets self.keys to WASD if the used clicks the WASD button
        """
        self.keys = "WASD"
    def useArrow(self):
        """
        sets self.keys to Arrow if the used clicks the Arrow button
        """
        self.keys = "Arrow"

saveFile = len(open("Save.txt").readline())

height, width = 768, 1366

menus = Menu()
canvas = tk.Canvas(menus.menu, height = height, width = width, bg="black")
canvas.pack()
menus.setWindow(width, height)
menus.background()
