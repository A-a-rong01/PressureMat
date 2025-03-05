import tkinter as tk
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
import threading

ports = serial.tools.list_ports.comports()
portsList = [str(port) for port in ports]

serialInst = None  # Global serial instance
selected_comport = None
selected_baud_rate = None

# Function to get selected COM port
def get_comport():
    global selected_comport
    selected_comport = comportSelectionLabel.get().strip()
    print("Selected COM Port:", selected_comport)

# Function to get selected baud rate
def get_baud_rate():
    global selected_baud_rate
    selected_baud_rate = baudRateDropdown.get().strip()
    print("Selected Baud Rate:", selected_baud_rate)

# Function to establish serial connection
def open_serial():
    global serialInst, selected_comport, selected_baud_rate
    
    if not selected_comport or not selected_baud_rate:
        print("Please select a COM port and baud rate first.")
        return
    
    try:
        serialInst = serial.Serial(port=selected_comport, baudrate=int(selected_baud_rate), timeout=1)
        print(f"Connected to {selected_comport} at {selected_baud_rate} baud.")
        
        # Start a separate thread for reading serial data
        threading.Thread(target=read_serial, daemon=True).start()
        
    except Exception as e:
        print(f"Error opening serial port: {e}")

# Function to continuously read data from serial port
def read_serial():
    global serialInst
    while True:
        if serialInst and serialInst.in_waiting:
            try:
                packet = serialInst.readline().decode('utf-8').strip()
                print("Received:", packet)
            except Exception as e:
                print(f"Error reading serial data: {e}")

# Function to plot data
def plot():
    if selected_comport and selected_baud_rate:
        data = np.random.random((12,12))
        plt.imshow(data, cmap='viridis')
        plt.title("2-D Heat Map")
        plt.colorbar()
        plt.show()

# Function to exit program
def Exit():
    if serialInst:
        serialInst.close()
    window.quit()

# GUI Settings
ctk.set_appearance_mode("system")

# Creating the Window
window = ctk.CTk()
window.title('B EE 484 - Pressure Sensor Project')
window.geometry('500x600')

# Title Label
introLabel = ctk.CTkLabel(
    master=window, 
    text="B EE 484 - Pressure Sensor Project", 
    font=("Arial", 24, "bold"),
    text_color="white"
)
introLabel.pack(pady=15)

# COM Port Selection
comportIntro = ctk.CTkLabel(master=window, text="Available COM Ports:")
comportIntro.pack()

for port in portsList:
    comportLabel = ctk.CTkLabel(master=window, text=port)
    comportLabel.pack()

comportFrame = ctk.CTkFrame(master=window)
comportFrame.pack(pady=10)

comportSelectionLabel = ctk.CTkEntry(master=comportFrame, placeholder_text="Enter COM Port", width=200)
comportSelectionLabel.pack(side="left", padx=10)

comportSelectButton = ctk.CTkButton(master=comportFrame, text="Enter COM Port", command=get_comport)
comportSelectButton.pack(side="left")

# Baud Rate Selection
baudRateFrame = ctk.CTkFrame(master=window)
baudRateFrame.pack(pady=10)

baud_rates = ["9600", "2400", "4800", "19200", "38400", "57600", "115200"]
baudRateDropdown = ctk.CTkComboBox(master=baudRateFrame, values=baud_rates)
baudRateDropdown.pack(side="left")

selectButton = ctk.CTkButton(master=baudRateFrame, text="Select Baud Rate", command=get_baud_rate)
selectButton.pack(side="left")

# Serial Connection Button
connectButton = ctk.CTkButton(master=window, text="Open Serial Connection", command=open_serial)
connectButton.pack(pady=5)

# Plot Button
plotButton = ctk.CTkButton(master=window, text="Plot", command=plot)
plotButton.pack(pady=5)

# Exit Button
exitButton = ctk.CTkButton(master=window, text="Exit", command=Exit)
exitButton.pack(pady=5)

# Start GUI Loop
window.mainloop()
