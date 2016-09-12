#!/usr/bin/python

__author__ = 'Wei'
from Tkinter import *
import Tkinter as tk
import tkMessageBox

class ScrolledText(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, *args, **kwargs)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        # expose some text methods as methods on this object
        self.insert = self.text.insert
        self.delete = self.text.delete
        self.mark_set = self.text.mark_set
        self.get = self.text.get
        self.index = self.text.index
        self.search = self.text.search
	
class inputCellE (tk.Frame):
    def __init__(self, parent, ltxt, default):
	tk.Frame.__init__(self, parent, class_='inputCellE')
	self.pack(side=TOP)
	self.creatWidget(ltxt, default)
	self.get = self.p.get
    def creatWidget(self, ltxt, default):
        self.l = Label(self, text=ltxt, width=10, anchor=E, padx=5)
        self.l.pack(side=LEFT)
        self.p = Entry(self)
        self.p.insert(1, default)
        self.p.pack(side=RIGHT)

class inputCellLB (tk.Frame):
    def __init__(self, parent, ltxt, alist):
	tk.Frame.__init__(self, parent, class_='inputCellLB')
	self.pack(side=TOP)
	self.creatWidget(ltxt, alist)
	self.get = self.p.get
    def creatWidget(self, ltxt, alist):
        self.l = Label(self, text=ltxt, width=10, anchor=E, padx=5)
        self.l.pack(side=LEFT)
        self.p = Listbox(self)
        self.p.insert(END, *alist)
        self.p.pack(side=RIGHT)

class inputCellOM (tk.Frame):
    def __init__(self, parent, ltxt, alist):
	tk.Frame.__init__(self, parent, class_='inputCellOM')
	self.pack(side=TOP)
	self.creatWidget(ltxt, alist)
	self.get = self.v.get
    def creatWidget(self, ltxt, alist):
        self.l = Label(self, text=ltxt, width=10, anchor=E, padx=5)
        self.l.pack(side=LEFT)
	self.v = StringVar()
        self.v.set(alist[0])
        self.p = OptionMenu(self, self.v, *alist)
        self.p.pack(side=RIGHT)

class mainWin (tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, class_='mainWin')
        self.pack(fill=BOTH, expand=TRUE)
        self.creatMenu(parent)
        self.creatWidget()
    def creatWidget(self):
        pw1 = PanedWindow(self) 
        pw1.pack(fill=BOTH, expand=1)
        frameInput = LabelFrame(pw1, text="SCom Parameters", height=200, width=30)
        frameInput.pack(fill="both", expand="yes")
        pw1.add(frameInput)
        self.port = inputCellE(frameInput, "Port:", "COM1")
        self.baudrate = inputCellE(frameInput, "Baudrate:", "19200")
        #FIVEBITS(5), SIXBITS(6), SEVENBITS(7), EIGHTBITS(8)
        self.bytesize = inputCellE(frameInput, "DataBits:", "8") 
        #PARITY_NONE(N), PARITY_EVEN(E), PARITY_ODD(O), PARITY_MARK(M), PARITY_SPACE(S)
        self.parity = inputCellE(frameInput, "Parity:", "N")
        #STOPBITS_ONE(1), STOPBITS_ONE_POINT_FIVE(1.5), STOPBITS_TWO(2)
        self.stopbits = inputCellE(frameInput, "StopBits:", "1")
        self.timeout = inputCellE(frameInput, "Timeout(s):", "10")
        fc_items = ('NONE', 'XONXOFF', 'RTSCTS', 'DSRDTR')
        self.flowctrl = inputCellOM(frameInput, "FlowCtrl:", fc_items)
        
        pw2 = PanedWindow(pw1, orient=VERTICAL)
        pw1.add(pw2)
        frameTransmitted = LabelFrame(pw2, text="Transmitted", width=800, height=100)
        self.entry_tx = Entry(frameTransmitted)
        self.entry_tx.pack(side=LEFT, fill=X, expand=1)
        button_tx = Button(frameTransmitted, text='Send', command=do_tx)
        button_tx.pack(side=RIGHT)
        pw2.add(frameTransmitted)
        frameReceived = LabelFrame(pw2, text="Received", width=800)
        self.text_recv = ScrolledText(frameReceived)
        self.text_recv.pack(side=TOP, fill=BOTH, expand=1)
        pw2.add(frameReceived)
    def creatMenu(self, parent):
        menubar = Menu(self)
        filemenu = Menu(menubar,tearoff=0)
        filemenu.add_command(label="Open", command=open)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=rootWin.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        parent.config(menu=menubar)

def about():
    tkMessageBox.showinfo("About", "Serial COM Port Configuration & Test Tool\ndesigned by Wei in Sep 2016\nEmail: futurewayne@gmail.com")
	
def open():
	tkMessageBox.showinfo("Open SCom Configuration...", "not implemented yet")
	
def do_tx():
	print "Start Tx now..."
	print "COM port: %s" % mywin.port.get()
	print "Baudrate: %s" % mywin.baudrate.get()

rootWin = tk.Tk()
rootWin.title('Serial COM Port Configuration & Test')
mywin = mainWin(rootWin)
rootWin.mainloop()
