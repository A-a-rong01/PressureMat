
import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

com = input("Select Com Port for Arduino")

for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print(use)

serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

data = np.random.random((12,12))

while True: 
    command = input("Arduino Command (ON/OFF/blink/exit): ")
    serialInst.write(command.encode('utf-8'))
     
    if command == 'exit':
        exit()



data = np.random.random((12,12))
plt.imshow(data)

plt.title("2-D Heat Map")
plt.show()