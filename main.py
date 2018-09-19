#!/usr/bin/env/ python

from Tkinter import *
import tkFileDialog
import timeit
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

from datetime import datetime
import AS7262_Pi as spec
import csv

#Setup Hardware
spec.soft_reset()
spec.set_gain(3)
spec.set_integration_time(100) #X2.8ms
spec.set_measurement_mode(3)
#spec.enable_main_led()
#spec.disable_main_led()

continuePlotting = False

channels = [
    ("red", 0),
    ("orange", 1),
    ("yellow", 2),
    ("green", 3),
    ("blue", 4),
    ("purple", 5)
]
#initialize variables
c = 1
count = 1
global t
t = []
global l
l= []
global start_time
start_time= time.time()

def save_file():
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv")
    if f is None:
        return
    
    f.write('AS7262 Channel Test: ' + str(channels[v.get()][0]) + '\n')
    f.write('time date: \n')
    f.write('time(s)   | intensity \n')

    for line in l:
        for time in t:
            f.write(str(time) + '\t' + str(line) + '\n')
    f.close()


def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True
	start_time = time.time()

def data_points(v):

    results = spec.take_single_measurement() #get_calibrated_value
    global elapsed_time
    elapsed_time = time.time() - start_time
    print('elapsed time, start_time: '+ str(elapsed_time) +','+ str(start_time))
    intensity = results[v]
    l.append(intensity)
    t.append(elapsed_time)
       
    return l, t, elapsed_time 

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
    for color, color_val in channels:
       radio = Radiobutton(root, text=color, variable=v, value=color_val).pack(side=LEFT, padx=4, pady=5) #command = function called when radio button changed
	
	#w = Checkbutton(root, 
    #chan = Checkbar(root, channels)
    #chan.pack(side=LEFT)

    #print(list(chan.state()))

    Label(root, text="Port:", bg='gray').pack(side=LEFT)
    global port
    port = Entry(root).pack(side=LEFT)
    Label(root, text="(ex: /dev/ttyUSB0)", bg='gray').pack(side=LEFT)

    def plotter():

        while continuePlotting:
            ax.cla()
            ax.grid()
            dpts = data_points(v.get())
            ax.plot(t, l, color=channels[v.get()][0])
            ax.set_xlabel('time(s)')
	    ax.set_ylabel('intensity')
            graph.draw()

    def clear_plot():
        ax.cla()
        ax.grid()
        graph.draw()
        #del t[:]
	l.clear()
	t.clear()
	#start_time = elapsed_time
        #print(start_time)
	#print('cleared')
        #return l, t, start_time
 
    def gui_handler():
	change_state()
        threading.Thread(target=plotter).start()

    e = Button(root, text="Exit", command=root.destroy, bg="red").pack(side=RIGHT)
    s = Button(root, text="Save", command=save_file, bg="blue", fg="white").pack(side=RIGHT)
    c = Button(root, text ='Clear', command = clear_plot, bg="orange").pack(side=RIGHT)
    b = Button(root, text="Start/Stop", command=gui_handler, bg="green", fg="white").pack(side=RIGHT)


    root.mainloop()


if __name__ == '__main__':
    app(channels)
