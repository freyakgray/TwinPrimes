from tkinter import *
from tkinter import ttk
import TwinPrimes as tp

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)

        # member variables
        self.int_var = IntVar(self)
        self.str_var = StringVar(self)
        self.entry = Entry(self, width=7, textvariable=self.int_var)
        self.str_entry = Entry(self, width=7, textvariable=self.str_var)
        self.function_labels = []
        self.selected_functions = {
            "View Critical Area": False, 
            "Find Average Gap": False,
            "Valid Coordinates": False,
            "Generate Combo": False,
            "View Combo": False,
            "View Crit Combos": False,
            "Generate Combos": False,
            "Valid Num Approx": False,
        }
        self.functions = list(self.selected_functions.keys())
        self.selection_entries = []
        self.selection_inputs = []
        self.inputs_for_run = {}

        # message file
        with open("Welcome.txt", "r") as f:
            msg = f.read()

        # labels
        welcome = Label(self, text=msg)

        # buttons
        self.generateHexas = Button(self, text="Generate Hexas", command=self.getHexasNum)

        self.genHexasList = Button(self, name="genHexasList", text="Submit", 
            command=lambda: [tp.GenerateHexas(int(self.entry.get())), 
                            self.displayFunctions(),
                            self.removeEntry(),
                            self.generateHexas.destroy(),
                            self.genHexasList.destroy(),
                            welcome.destroy()])

        # pack
        welcome.grid(row=0, column=0)
        self.generateHexas.grid(row=1, column=0)
        

    def getHexasNum(self):
        self.entry.grid(row=2, column=0)
        self.int_var.set("")
        self.genHexasList.grid(row=3, column=0)


    def displayFunctions(self):
        bools = []
        vca = BooleanVar()
        Checkbutton(self, text=self.functions[0], variable=vca).grid(row=0, column=0)
        find_gap = BooleanVar()
        Checkbutton(self, text=self.functions[1], variable=find_gap).grid(row=1, column=0)
        valid_coord = BooleanVar()
        Checkbutton(self, text=self.functions[2], variable=valid_coord).grid(row=2, column=0)
        generate_combo = BooleanVar()
        Checkbutton(self, text=self.functions[3], variable=generate_combo).grid(row=3, column=0)
        view_combo = BooleanVar()
        Checkbutton(self, text=self.functions[4], variable=view_combo).grid(row=4, column=0)
        view_crit_combos = BooleanVar()
        Checkbutton(self, text=self.functions[5], variable=view_crit_combos).grid(row=5, column=0)
        generate_combos = BooleanVar()
        Checkbutton(self, text=self.functions[6], variable=generate_combos).grid(row=6, column=0)
        valid_num_approx = BooleanVar()
        Checkbutton(self, text=self.functions[7], variable=valid_num_approx).grid(row=7, column=0)

        bools.append(vca)
        bools.append(find_gap)
        bools.append(valid_coord)
        bools.append(generate_combo)
        bools.append(view_combo)
        bools.append(view_crit_combos)
        bools.append(generate_combos)
        bools.append(valid_num_approx)

        i = 0
        for k in self.selected_functions:
            self.selected_functions[k] = bools[i]
            i += 1
        
        Button(self, text="Confirm", command=self.getSelections).grid(row=8, column=0)

    
    def getSelections(self):
        self.selection_inputs.clear()
        self.inputs_for_run.clear()

        for l in self.function_labels:
            l.destroy()
        for e in self.selection_entries:
            e.destroy()
        r = 9
        for k in self.selected_functions:
            if self.selected_functions[k].get():
                if k == "View Critical Area":
                    label = Label(self, text=k + " --> run to view")
                    self.inputs_for_run[k] = 0
                    self.function_labels.append(label)
                    label.grid(row=r, column=0)
                elif k == "Find Average Gap":
                    label = Label(self, text=k + " --> hexasChecked: ")
                    find_avg = IntVar()
                    e = Entry(self, width=7, textvariable=find_avg)
                    self.selection_entries.append(e)
                    e.grid(row=r, column=1)
                    self.selection_inputs.append(find_avg)
                    self.inputs_for_run[k] = find_avg
                    self.function_labels.append(label)
                    label.grid(row=r, column=0)
                elif k == "Valid Coordinates":
                    label = Label(self, text=k + " --> hexasNum: ")
                    valid_coord = IntVar()
                    e = Entry(self, width=7, textvariable=valid_coord)
                    self.selection_entries.append(e)
                    e.grid(row=r, column=1)
                    self.selection_inputs.append(valid_coord)
                    self.inputs_for_run[k] = valid_coord
                    self.function_labels.append(label)
                    label.grid(row=r, column=0)
                elif k == "Generate Combo":
                    label1 = Label(self, text=k + " --> hexasChecked: ")
                    generate_combo_input1 = IntVar()
                    generate_combo_input2 = IntVar()
                    label1.grid(row=r, column=0)

                    multi_entry = []

                    e1 = Entry(self, width=7, textvariable=generate_combo_input1)
                    self.selection_entries.append(e1)
                    e1.grid(row=r, column=1)

                    label2 = Label(self, text=" index: ")
                    label2.grid(row=r, column=2)
                    e2 = Entry(self, width=7, textvariable=generate_combo_input2)
                    self.selection_entries.append(e2)
                    e2.grid(row=r, column=3)

                    self.selection_inputs.append(generate_combo_input1)
                    self.selection_inputs.append(generate_combo_input2)

                    multi_entry.append(generate_combo_input1)
                    multi_entry.append(generate_combo_input2)

                    self.inputs_for_run[k] = multi_entry
                
                    self.function_labels.append(label1)
                    self.function_labels.append(label2)

                elif k == "View Combo":
                    label1 = Label(self, text=k + " --> hexasChecked: ")

                    view_combo_input1 = IntVar()
                    view_combo_input2 = IntVar()
                    view_combo_input3 = IntVar()

                    label1.grid(row=r, column=0)

                    multi_entry = []

                    e1 = Entry(self, width=7, textvariable=view_combo_input1)
                    self.selection_entries.append(e1)
                    e1.grid(row=r, column=1)

                    label2 = Label(self, text=" start: ")
                    label2.grid(row=r, column=2)
                    e2 = Entry(self, width=7, textvariable=view_combo_input2)
                    self.selection_entries.append(e2)
                    e2.grid(row=r, column=3)

                    label3 = Label(self, text=" length: ")
                    label3.grid(row=r, column=4)
                    e3 = Entry(self, width=7, textvariable=view_combo_input3)
                    self.selection_entries.append(e3)
                    e3.grid(row=r, column=5)

                    self.selection_inputs.append(view_combo_input1)
                    self.selection_inputs.append(view_combo_input2)
                    self.selection_inputs.append(view_combo_input3)

                    multi_entry.append(view_combo_input1)
                    multi_entry.append(view_combo_input2)
                    multi_entry.append(view_combo_input3)

                    self.inputs_for_run[k] = multi_entry
                
                    self.function_labels.append(label1)
                    self.function_labels.append(label2)
                    self.function_labels.append(label3)
                elif k == "View Crit Combos":
                    label = Label(self, text=k + " --> hexasChecked: ")
                    view_crit_combos = IntVar()
                    e = Entry(self, width=7, textvariable=view_crit_combos)
                    self.selection_entries.append(e)
                    e.grid(row=r, column=1)
                    self.selection_inputs.append(view_crit_combos)
                    self.inputs_for_run[k] = view_crit_combos
                    self.function_labels.append(label)
                    label.grid(row=r, column=0)
                elif k == "Generate Combos":
                    label = Label(self, text=k + " --> hexasNum: ")
                    generate_combos = IntVar()
                    e = Entry(self, width=7, textvariable=generate_combos)
                    self.selection_entries.append(e)
                    e.grid(row=r, column=1)
                    self.selection_inputs.append(generate_combos)
                    self.inputs_for_run[k] = generate_combos
                    self.function_labels.append(label)
                    label.grid(row=r, column=0)
                elif k == "Valid Num Approx":
                    label = Label(self, text=k + " --> hexasNum: ")
                    valid_num_approx = IntVar()
                    e = Entry(self, width=7, textvariable=valid_num_approx)
                    self.selection_entries.append(e)
                    e.grid(row=r, column=1)
                    self.selection_inputs.append(valid_num_approx)
                    self.inputs_for_run[k] = valid_num_approx
                    self.function_labels.append(label)
                    label.grid(row=r, column=0)

                    
            r += 1
        if len(self.selected_functions) > 0:
            Button(self, text="Run", command=self.run).grid(row=r, column=0)
        

    def run(self):

        for k in self.inputs_for_run:
            if k == "View Critical Area":
                tp.ViewCritArea()
            elif k == "Find Average Gap":
                tp.FindAverageGap(int(self.inputs_for_run[k].get()))
            elif k == "Valid Coordinates":
                tp.ValidCoordinates(int(self.inputs_for_run[k].get()))
            elif k == "Generate Combo":
                tp.GenerateCombo(self.inputs_for_run[k][0].get(), self.inputs_for_run[k][1].get())
            elif k == "View Combo":
                tp.ViewCombo(self.inputs_for_run[k][0].get(), self.inputs_for_run[k][1].get(), self.inputs_for_run[k][2].get())
            elif k == "View Crit Combos":
                tp.ViewCritCombos(int(self.inputs_for_run[k].get()))
            elif k == "Generate Combos":
                tp.GenerateCombos(int(self.inputs_for_run[k].get()))
            elif k == "Valid Num Approx":
                tp.ValidNumApproximation(int(self.inputs_for_run[k].get()))
            

    def removeEntry(self):
        self.entry.delete(0, END)
        self.entry.grid_forget()

    
    def setEntry(self):
        self.entry.grid(row=0, column=0)
        self.int_var.set("")


if __name__ == "__main__":
    gui = GUI()
    gui.title("Twin Primes")
    gui.geometry("600x400")
    gui.mainloop()