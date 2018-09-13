import matplotlib.pyplot as plt
import numpy as np
from time import time

# Import the script for the board
import AS7262_Pi as spec
from datetime import datetime

filename = datetime.now().strftime("%Y%m%d-%H:%m")
file = open(filename + '.txt', 'w')

# Reboot the spectrometer, just in case
spec.soft_reset()

# Set the gain of the device between 0 and 3.  Higher gain = higher readings
spec.set_gain(3)  # 3=x64

# Set the integration time between 1 and 255.  Higher means longer readings
spec.set_integration_time(255)  # x2.8ms

# Set the board to continuously measure all colours
spec.set_measurement_mode(2)

# Settings for plot
# channels = ('Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet')
channels = ('Green')
y_pos = 1  # np.arange(len(channels))

plt.ion()
fig, (ax0, ax1) = plt.subplots(nrows=2)

# file.write('Time(s)  |	Violet  |  Blue  |   Green   |	Yellow	 |  Orange   |	Red\n')
# file.write('_________________________________________________________________________\n')


file.write('time(s)	Green\n')
# Run this part of the script until stopped with control-C
try:
    # Turn on the main LED
    # spec.enable_main_led()
    start_time = time()

    while True:
        intensity = []
        # Store the list of readings in the variable "results"
        results = spec.get_calibrated_values()
        elapsed_time = time() - start_time

        # Print the results!
        print('Elapsed Time ' + str(elapsed_time))
        # print("Red    :" + str(results[0]))
        # print("Orange :" + str(results[1]))
        # print("Yellow :" + str(results[2]))
        print("Green  :" + str(results[3]))
        # print("Blue   :" + str(results[4]))
        # print("Violet :" + str(results[5]) + "\n")

        # R = results[0]
        # O = results[1]
        # Y = results[2]
        G = results[3]
        # B = results[4]
        # V = results[5]

        # intensity.append(V)
        # intensity.append(B)
        # intensity.append(G)
        # intensity.append(Y)
        # intensity.append(O)
        # intensity.append(R)

        intensity = G

        ax0.cla()
        ax1.cla()

        line = ax0.plot(intensity)

        line1 = ax1.bar(y_pos, intensity)  # , align='center')
        # line1[0].set_color('m')
        # line1[1].set_color('b')
        line1[0].set_color('g')
        # line1[3].set_color('y')
        # line1[4].set_color('c')
        # line1[5].set_color('r')


        ax0.set_title('AS7262 Line')  # xticks(y_pos, channels)
        ax0.set_ylabel('intensity')

        # ax1.set_xticklabels(channels)

        # plt.xticks(y_pos, channels)
        plt.ylabel('intensity')
        plt.title('AS7262 Line')

        fig.canvas.draw()

        file.write(str(elapsed_time) + '\t' + str(
            G) + '\n')  # +'\t'+str(B)+'\t'+str(G)+'\t'+str(Y)+'\t'+str(O)+'\t'+str(R)+ '\n')

# When the script is stopped with control-C
except KeyboardInterrupt:
    # Set the board to measure just once (it stops after that)
    spec.set_measurement_mode(3)
    # Turn off the main LED
    # spec.disable_main_led()
    file.close()
    # Notify the user
    print("Manually stopped")
