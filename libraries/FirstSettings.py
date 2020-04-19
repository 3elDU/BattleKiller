from tkinter import *


class Main:
    def __init__(self):
        self.root = Tk()
        self.root.title("Settings")

        self.pX = None
        self.pY = None

        self.lbl1 = Label(text='Block size multiplier')
        self.lbl1.pack(side=TOP, padx=100, pady=10)

        self.f1 = Frame()

        self.lbl2 = Label(self.f1, text='(default is 16x16)')
        self.e1 = Entry(self.f1, width=3)
        self.e2 = Entry(self.f1, width=3)

        self.empty1 = Label(self.f1, text='')
        self.empty2 = Label(self.f1, text='')

        self.lbl2.pack(side=LEFT)
        self.e1.pack(side=LEFT)
        self.e2.pack(side=LEFT)
        self.empty1.pack(side=TOP)
        self.empty2.pack(side=TOP)

        self.f1.pack(side=TOP)

        self.f2 = Frame()

        self.savebtn = Button(self.f2, text='Save')

        self.savebtn.pack(side=LEFT, padx=10, pady=10)

        self.f2.pack(side=TOP)

        self.savebtn['command'] = self.save

        self.root.mainloop()

    def save(self):
        self.pX = int(self.e1.get())
        self.pY = int(self.e2.get())
        self.root.destroy()

    def getSizes(self):
        return self.pX, self.pY
