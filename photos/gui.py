import Tkinter as tk
from tkFileDialog import askopenfilename

class Gui(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        
        self.entry = tk.Entry(self)
        self.entry.grid(column=0, row=0, sticky='nw')
        self.entry.grid(column=1, row=0, sticky='ne')
        self.entry.grid(column=1, row=1, sticky='se')
        self.entry.grid(column=0, row=1, sticky='sw')
        self.entry.bind('<Return>', self.onPressEnter)

        in_button = tk.Button(self, text='Image', command=self.onInButtonClick)
        in_button.grid(column=0, row=0)

        data_button = tk.Button(self, text='Data', command=self.onDataButtonClick)
        data_button.grid(column=1, row=0)
        
        self.in_label_variable = tk.StringVar()
        in_label = tk.Label(self, textvariable=self.in_label_variable, 
                anchor='w', fg='white', bg='blue')
        in_label.grid(column=0, row=1, columnspan=1, sticky='ew')

        self.data_label_variable = tk.StringVar()
        data_label = tk.Label(self, textvariable=self.data_label_variable, 
                anchor='e', fg='white', bg='blue')
        data_label.grid(column=1, row=1, columnspan=1, sticky='ew')

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, True)

    def onInButtonClick(self):
        filename = askopenfilename()
        self.in_label_variable.set(filename.split('/')[-1])
    
    def onDataButtonClick(self):
        filename = askopenfilename()
        self.data_label_variable.set(filename.split('/')[-1])

    def onPressEnter(self, event):
        self.in_label_variable.set('You pressed enter')

if __name__ == '__main__':
    app = Gui(None)
    app.title('GUI frontend for steganography')
    app.mainloop()
