from tkinter import *


class Main:
    def __init__(self):
        self.root = Tk()
        self.root.title("Choose rules")

        self.mapf = Frame()
        self.mapl = Label(self.mapf, text="Map name: ")
        self.mape = Entry(self.mapf, width=16)

        self.mapl.pack(side=LEFT)
        self.mape.pack(side=LEFT)
        self.mapf.pack(padx=40, pady=10, side=TOP)

        self.hpf = Frame()
        self.hpl = Label(self.hpf, text="Hp multiplier: ")
        self.hpe = Entry(self.hpf, width=3)

        self.hpl.pack(side=LEFT)
        self.hpe.pack(side=LEFT)
        self.hpf.pack(padx=40, pady=10, side=TOP)

        self.amf = Frame()
        self.aml = Label(self.amf, text="Ammo multiplier: ")
        self.ame = Entry(self.amf, width=2)

        self.aml.pack(side=LEFT)
        self.ame.pack(side=LEFT)
        self.amf.pack(side=TOP)

        self.okbtn = Button(text='OK')
        self.okbtn.pack(padx=10, pady=30, side=TOP)

        self.okbtn['command'] = self.ok

        self.root.mainloop()

    def ok(self):
        self.root.destroy()

    def getRules(self):
        toReturn = []
        toReturn += self.mape.get()
        toReturn += int(self.hpe.get())
        toReturn += int(self.ame.get())
        return toReturn
