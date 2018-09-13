from Tkinter import *
from random import randint


# these four imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading
from serial import Serial

from time import time
from datetime import datetime
import AS7262_Pi as spec

#Setup Hardware
spec.soft_reset()
spec.set_gain(3)
spec.set_integration_time(255) #X2.8ms
spec.set_measurement_mode(3)

continuePlotting = False

data = [1,2,3,4,5,6,7,8,8,9,2,4,2,66,4,3,2]
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

def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True

def read_data():
    line = ser.readline()
    print line


def data_points(start_time, l, t):#, color_val): ,line

    results = spec.get_calibrated_values()
    elapsed_time = time.time() - start_time()

    #f = open("data.txt", "w")
    intensity = results[channel]

    l.append(int(intensity))
    t.append(elapsed_time)
    #for i in range(len(data)):
    #    l.append(int(data[i].rstrip("\n")))

    #l = data[0:count]

    return l


def app(channels):
    # initialise a window.
    root = Tk()
    root.config(background='gray')
    root.geometry("1000x700")
    root.title("AS7262 Data Collection")
    # radio buttons for color channel
    #c = IntVar()
    #c.set(1)

    Label(root, text="Multi-Channel Serial Plotting", bg='gray').pack()

    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()


    graph = FigureCanvasTkAgg(fig, master=root)

    graph.get_tk_widget().pack(side="top", fill='both', expand=True)

    global color_val
    for color, color_val in channels:
        Radiobutton(root, text=color, value=color_val).pack(side=LEFT, padx=4, pady=5)#grid(row=16, column=val+1) #command = function called when radio button changed

    Label(root, text="Port:", bg='gray').pack(side=LEFT)
    global port
    port = Entry(root).pack(side=LEFT)
    Label(root, text="(ex: /dev/ttyUSB0)", bg='gray').pack(side=LEFT)

    def plotter():

        while continuePlotting:
            ax.cla()
            ax.grid()
            global count
            #dpts = data_points()
            dpts = l

            #ax.plot(range(10), dpts, marker='o', color='orange')
            ax.plot(t,l, color='black')#range(len(dpts)), dpts, marker='o', color='orange')
            graph.draw()
            time.sleep(.1)
            count += 1


    def gui_handler():
        #global ser
        #ser = Serial(port, baudrate=9600)
        change_state()
        threading.Thread(target=plotter).start()

    def save():
        pass

    e = Button(root, text="Exit", command=root.destroy, bg="red").pack(side=RIGHT)
    s = Button(root, text="Save", command=save, bg="blue", fg="white").pack(side=RIGHT)
    b = Button(root, text="Start/Stop", command=gui_handler, bg="green", fg="white").pack(side=RIGHT)


    root.mainloop()


if __name__ == '__main__':
    app(channels)
