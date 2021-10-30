from tkinter import *
import TwinPrimes as tp

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)

        # member variables
        self.entry = Entry(self)
        self.int_var = IntVar(self)
        
        # buttons
        self.generateHexas = Button(self, text="Generate Hexas", command=self.getHexasNum)
        self.retrieveHexasList = Button(self, text="Retrieve Hexas", command=self.getHexasList)

        # pack
        self.generateHexas.pack()
        self.retrieveHexasList.pack()
        


    def getHexasNum(self):
        self.entry = Entry(self, width=5, textvariable=self.int_var)
        self.entry.pack()
        self.int_var.set("")
        self.submit(tp.GenerateHexas, self.entry)
        self.hexasGenerated = True
        

    def submit(self, action, e):
        return Button(self, text="submit", command=lambda: action(int(e.get()))).pack()


    def getHexasList(self):
        print(tp.hexasList)


gui = GUI()

gui.title("Twin Primes")
gui.geometry("600x400")

gui.mainloop()