from tkinter import *


class Main:
    def __init__(self):
        self.choose = 2

        self.root = Tk()
        self.root.title("Choose game mode:")

        self.lbl = Label(text='Choose mode: ')
        self.lbl.pack(side=TOP, padx=10, pady=20)

        self.buttonsFrame = Frame()

        self.serverbtn = Button(self.buttonsFrame, text='Server')
        self.exitbtn = Button(self.buttonsFrame, text='Exit')
        self.clientbtn = Button(self.buttonsFrame, text='Client')

        self.serverbtn.pack(side=LEFT, padx=10, pady=10)
        self.exitbtn.pack(side=LEFT, padx=0, pady=10)
        self.clientbtn.pack(side=LEFT, padx=10, pady=10)

        self.buttonsFrame.pack(padx=50, side=TOP)

        self.serverbtn['command'] = self.chooseServer
        self.exitbtn['command'] = self.exit
        self.clientbtn['command'] = self.chooseClient

        self.root.mainloop()

    def exit(self):
        self.choose = 2
        self.root.destroy()

    def chooseClient(self):
        self.choose = 1
        self.root.destroy()

    def chooseServer(self):
        self.choose = 0
        self.root.destroy()

    def getChosen(self):
        return self.choose
