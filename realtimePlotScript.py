import serial

import numpy as np

import matplotlib.pyplot as plt

import matplotlib.animation as animation


# Adjust for ESP32 Serial Port

port = "COM9"

baud_rate = 115200

rows, cols = 9, 9


ser = serial.Serial(port, baud_rate, timeout=1)


def read_serial_data():

    data = []

    while True:

        line = ser.readline().decode().strip()

        if line == "START":

            data = []

        elif line == "END":

            matrix = np.array(data, dtype=int)

            # Flip the matrix horizontally

            matrix_flipped = np.flip(matrix, axis=1)

            return matrix_flipped

        else:

            row_data = [int(x) for x in line.split(",")]

            if len(row_data) == cols:

                data.append(row_data)

                


def update(frame):

    sensor_data = read_serial_data()

    if sensor_data.shape == (rows, cols):

        heatmap.set_data(sensor_data)

    return [heatmap]


fig, ax = plt.subplots()

heatmap = ax.imshow(np.zeros((rows, cols)), cmap="inferno", vmin=0, vmax=2000)

plt.colorbar(heatmap)


ani = animation.FuncAnimation(fig, update, interval=10, blit=False)

plt.show()