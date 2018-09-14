#!/usr/bin/env/ python

from Tkinter import *
from random import randint
#sudo easy_install pydaqflex
#pip install pydaqflex
#import daqflex
#dev=daqflex.USB_204
#print(dev)

# these four imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading
from serial import Serial

from datetime import datetime
import AS7262_Pi as spec
import csv

#Setup Hardware
spec.soft_reset()
spec.set_gain(3)
spec.set_integration_time(100) #X2.8ms
spec.set_measurement_mode(3)
#spec.enable_main_led()

continuePlotting = False

#data = [1,2,3,4,5,6,7,8,8,9,2,4,2,66,4,3,2]
channels = [
    ("Red", 0),
    ("Orange", 1),
    ("Yellow", 2),
    ("Green", 3),
    ("Blue", 4),
    ("Violet", 5)
]
#initialize variables
c = 1
count = 1
global t
t = []
global l
l= []

def save_file():
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv")
    if f is None:
        return
    for line in data:
        f.write(str(line) + '\n')
    f.close()


def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True

def data_points(start_time, l, t, v):

    results = spec.take_single_measurement() #get_calibrated_values()
    
    try:
        #results = spec.get_calibrated_values()
        #elapsed_time = time.time() - start_time()
        elapsed_time = time.time()
        intensity = results[v]
        l.append(intensity)
        t.append(elapsed_time)
       
        return l, t

    except:
        return l, t 

class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
	Frame.__init__(self, parent)
	self.vars= []
	for pick in picks:
	    var = IntVar()
	    chk = Checkbutton(self, text=pick, variable=var)
	    chk.pack(side=side, anchor=anchor, expand = YES)
	    self.vars.append(var)

def app(channels):
    # initialise a window.
    root = Tk()
    root.config(background='gray')
    root.geometry("1000x700")
    root.title("AS7262 Data Collection")

    Label(root, text="Multi-Channel Serial Plotting", bg='gray').pack()
    global v
    v=IntVar()
    v.set(0)
    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()


    graph = FigureCanvasTkAgg(fig, master=root)

    graph.get_tk_widget().pack(side="top", fill='both', expand=True)

    global color_val
    #for color, color_val in channels:
       #radio = Radiobutton(root, text=color, variable=v, value=color_val).pack(side=LEFT, padx=4, pady=5) #command = function called when radio button changed
	#w = Checkbutton(root, 
    chan = Checkbar(root, channels)
    chan.pack(side=LEFT)

    print(list(chan.state()))

    Label(root, text="Port:", bg='gray').pack(side=LEFT)
    global port
    port = Entry(root).pack(side=LEFT)
    Label(root, text="(ex: /dev/ttyUSB0)", bg='gray').pack(side=LEFT)

    def plotter():

        while continuePlotting:
            ax.cla()
            ax.grid()
            dpts = data_points(start_time, l, t, v.get())

            #ax.plot(range(10), dpts, marker='o', color='orange')
            ax.plot(l, color='black')#range(len(dpts)), dpts, marker='o', color='orange')
            graph.draw()

    def gui_handler():
        global start_time
	start_time = time.time()
	change_state()
        threading.Thread(target=plotter).start()

    def save():
        pass

    e = Button(root, text="Exit", command=root.destroy, bg="red").pack(side=RIGHT)
    s = Button(root, text="Save", command=save_file, bg="blue", fg="white").pack(side=RIGHT)
    b = Button(root, text="Start/Stop", command=gui_handler, bg="green", fg="white").pack(side=RIGHT)


    root.mainloop()


if __name__ == '__main__':
    app(channels)
