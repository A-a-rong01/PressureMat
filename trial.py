import tkinter as tk
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
portsList = []
dataList = []
selected_comport = None
selected_baud_rate = None
rows, cols = 9, 9
ser = None

def get_comport():
    global selected_comport
    selected_comport = comportSelectionLabel.get()
    print("Entered COM Port:", selected_comport)

def get_baud_rate():
    global selected_baud_rate
    selected_baud_rate = baudRateDropdown.get()
    print("Selected Baud Rate:", selected_baud_rate)

def read_serial_data():
    global ser
    if ser is None:
        return np.zeros((rows, cols))
    
    data = []
    while True:
        line = ser.readline().decode().strip()
        if line == "START":
            data = []
        elif line == "END":
            matrix = np.array(data, dtype=int)
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

def plot():
    global ser
    if selected_comport and selected_baud_rate:
        try:
            ser = serial.Serial(selected_comport, int(selected_baud_rate), timeout=1)
            fig, ax = plt.subplots()
            global heatmap
            heatmap = ax.imshow(np.zeros((rows, cols)), cmap="inferno", vmin=0, vmax=2000)
            plt.colorbar(heatmap)
            ani = animation.FuncAnimation(fig, update, interval=10, blit=False)
            plt.show()
        except serial.SerialException as e:
            print("Error opening serial port:", e)

def Exit():
    if ser:
        ser.close()
    window.destroy()

ctk.set_appearance_mode("system")
window = ctk.CTk()
window.title('B EE 484 - Pressure Sensor Project')
window.geometry('500x500')

introLabel = ctk.CTkLabel(window, text="B EE 484 - Pressure Sensor Project", font=("Arial", 24, "bold"))
introLabel.pack(pady=15)

comportIntro = ctk.CTkLabel(window, text="Comports Listed:")
comportIntro.pack()

for one in ports:
    portsList.append(str(one))
    comportOne = ctk.CTkLabel(window, text=str(one))
    comportOne.pack()

comportFrame = ctk.CTkFrame(window)
comportFrame.pack(pady=10)

baudRateFrame = ctk.CTkFrame(window)
baudRateFrame.pack(pady=10)

comportSelectionLabel = ctk.CTkEntry(comportFrame, placeholder_text="Enter COM Port", width=200, height=30)
comportSelectionLabel.pack(side="left", padx=10)

comportSelectButton = ctk.CTkButton(comportFrame, text="Enter Comport", command=get_comport)
comportSelectButton.pack(side="left")

baud_rates = ["9600", "2400", "4800", "19200", "38400", "57600", "115200"]
baudRateDropdown = ctk.CTkComboBox(baudRateFrame, values=baud_rates)
baudRateDropdown.pack(pady=10, side="left")

selectButton = ctk.CTkButton(baudRateFrame, text="Select Baud Rate", command=get_baud_rate)
selectButton.pack(pady=10, side="left")

plotButton = ctk.CTkButton(window, text="Plot", command=plot)
plotButton.pack(pady=5)

exitButton = ctk.CTkButton(window, text="Exit", command=Exit)
exitButton.pack(pady=5)

window.mainloop()
