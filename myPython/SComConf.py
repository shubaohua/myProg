#!/usr/bin/python

__author__ = 'Wei'
from Tkinter import *
import Tkinter as tk
import tkMessageBox
import serial
import time
import thread
import traceback
import binascii

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
    def __init__(self, parent, ltxt, alist, default):
	# type: (object, object, object, object) -> object
	tk.Frame.__init__(self, parent, class_='inputCellOM')
	self.pack(side=TOP)
	self.creatWidget(ltxt, alist, default)
	self.get = self.v.get

    def creatWidget(self, ltxt, alist, default):
        self.l = Label(self, text=ltxt, width=10, anchor=E, padx=5)
        self.l.pack(side=LEFT)
	self.v = StringVar()
        self.v.set(default)
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
        self.port = inputCellOM(frameInput, "Port:", ser.port_list, ser.port_list[0])
        self.baudrate = inputCellE(frameInput, "Baudrate:", "19200")
        self.timeout = inputCellE(frameInput, "Timeout(s):", "5")
        self.bytesize = inputCellOM(frameInput, "DataBits:", ser.bytesize_list, ser.bytesize_list[3]) 
        self.parity = inputCellOM(frameInput, "Parity:", ser.parity_list, ser.parity_list[0])
        self.stopbits = inputCellOM(frameInput, "StopBits:", ser.stopbits_list, ser.stopbits_list[0])
        subframe1 = tk.Frame(frameInput)
        subframe1.pack(side=TOP)
        self.xonxoff = IntVar()
        cb_xonxoff = Checkbutton(subframe1, text="XON/XOFF", variable=self.xonxoff)
        cb_xonxoff.pack(side=LEFT)
        self.rtscts = IntVar()
        cb_rtscts = Checkbutton(subframe1, text="RTS/CTS", variable=self.rtscts)
        cb_rtscts.pack(side=RIGHT)
        self.inHex = IntVar()
        cb_inHex = Checkbutton(subframe1, text="inHEX", variable=self.inHex)
        cb_inHex.pack()
        self.isSerialEnabled = False
        self.text_button_en = StringVar()
        self.text_button_en.set('Serial Disabled')
        self.button_en = Button(frameInput, textvariable=self.text_button_en, command=do_en_serial, bg='red', activebackground='red')
        self.button_en.pack(side=TOP)
        
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
        filemenu.add_command(label="Exit", command=parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        parent.config(menu=menubar)

    def updateRxWin(self, aStr):
        self.text_recv.insert(tk.END, aStr)


def about():
    tkMessageBox.showinfo("About", "Serial COM Port Configuration & Test Tool\ndesigned by Wei in Sep 2016\nEmail: futurewayne@gmail.com")


def open():
    tkMessageBox.showinfo("Open SCom Configuration...", "not implemented yet")


def do_tx():
    txStr = mywin.entry_tx.get()
    ser.transmit(txStr)

def do_en_serial():
    if mywin.isSerialEnabled:
        mywin.isSerialEnabled = False
        mywin.text_button_en.set('Serial Disabled')
        mywin.button_en.configure(bg = 'red')
        mywin.button_en.configure(activebackground = 'red')
        ser.close_port()
    else:
        mywin.isSerialEnabled = True
        mywin.text_button_en.set('Serial Enabled')
        mywin.button_en.configure(bg = 'green')
        mywin.button_en.configure(activebackground = 'green')
        print "COM port: %s" % mywin.port.get()
        print "Baudrate: %d" % int(mywin.baudrate.get())
        print "Timeout: %d" % int(mywin.timeout.get())
        print "Bytesize: %d" % int(mywin.bytesize.get())
        print "Parity: %s" % mywin.parity.get()[0]
        print "Stopbits: %f" % int(mywin.stopbits.get())
        print "XONXOFF: %d" % mywin.xonxoff.get()
        print "RTSCTS: %d" % mywin.rtscts.get()
        print "inHEX: %d" % mywin.inHex.get()
        if False == ser.open_port(mywin.port.get(),
                    mywin.baudrate.get(),
                    int(mywin.timeout.get()),
                    int(mywin.bytesize.get()),
                    mywin.parity.get()[0],
                    int(mywin.stopbits.get()),
                    mywin.xonxoff.get(),
                    mywin.rtscts.get(),
                    mywin.inHex.get()):
            mywin.isSerialEnabled = False
            mywin.text_button_en.set('Serial Disabled')
            mywin.button_en.configure(bg='red')
            mywin.button_en.configure(activebackground='red')

class aSerial:
    port_list = ['NULL']
    parity_list = ('NONE', 'EVEN', 'ODD', 'MARK', 'SPACE')
    stopbits_list = ('1', '1.5', '2')
    bytesize_list= ('5', '6', '7', '8')

    def __init__(self):
        self.list_ports()
        self.isOpen = False
        self.rxStr = ''
        self.inHex = False
        self.rx_cnt = 0
        self.tx_cnt = 0
        self.crlf = 0
        self.sp = 'NULL'

    def __del__(self):
        self.isOpen = False
        time.sleep(1)
        self.close_port()

    def list_ports(self):
        import os
        if os.name == 'nt':
            from serial.tools.list_ports_windows import comports
        elif os.name == 'posix':
            from serial.tools.list_ports_posix import comports
        else:
            raise ImportError("Sorry: no implementation for your platform ('%s') available" % (os.name,))
        ports = sorted(comports())
        for n, (port, desc, hwid) in enumerate(ports, 1):
            self.port_list.append(port)

    def open_port(self, port, baudrate, timeout, bytesize, parity, stopbits, xonxoff, rtscts, inHex):
        if port != 'NULL':
            try:
                self.sp = serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize,
                                        parity=parity, stopbits=stopbits, xonxoff=xonxoff,
                                        rtscts=rtscts, timeout=timeout, write_timeout=timeout)
            except:
                traceback.print_exc()
                return False
            if self.sp.isOpen():
                print "%s is opened" % port
                self.isOpen = True
                self.inHex = inHex
            thread.start_new_thread(self.receive, ())
            return True
        else:
            print "Serial port is NULL"
            return False

    def close_port(self):
        self.isOpen = False
        time.sleep(1)
        if self.sp != 'NULL':
            self.sp.close()

    def receive(self):
        while self.isOpen == True:
            while ser.sp.inWaiting() > 0:
                rx = ser.sp.read(1)
                self.rx_cnt += 1
                self.rxStr += rx
                if rx == '\n':
                    continue
            if len(self.rxStr) > 0:
                if self.inHex:
                    aStr = binascii.hexlify(self.rxStr)
                else:
                    aStr = self.rxStr
                print "RX (%d bytes): %s" % (self.rx_cnt, aStr)
                mywin.updateRxWin(aStr)
                self.rxStr = ''
        else:
            print "Serial is closed. Receiving function exits."

    def transmit(self, aStr):
        print "aTX: %s" % aStr
        if self.inHex:
            try:
                bStr = binascii.unhexlify(aStr)
            except:
                traceback.print_exc()
                tkMessageBox.showinfo("Input Error","Need Even-length string for transmition in HEX mode!")
                return
        else:
            bStr = aStr + '\n'
            print "bTX: %s" % bStr
        ser.sp.write(bStr)

#def main():
ser = aSerial()
rootWin = tk.Tk()
rootWin.title('Serial COM Port Configuration & Test')
mywin = mainWin(rootWin)
rootWin.mainloop()

#if __name__ == "__main__":
#    main()
