import time
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


ports = serial.tools.list_ports.comports()
portsList = []
dataList = []

fig = plt.figure()
ax = fig.add_subplot(111)

time.sleep(2)

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

def animate(i, dataList):
    packet = serialInst.readline()
    newData = packet.decode('utf')

    try:
        newData = float(newData.strip())
        dataList.append(newData)

    except:
        pass

    dataList[:] = dataList[-50:]


    ax.clear()
    ax.plot(dataList)

    ax.set_ylim([0,5])
    ax.set_title("Arduino Data")
    ax.set_ylabel("Value")

while True: 
    # command = input("Arduino Command (ON/OFF/start/exit): ")
    # serialInst.write(command.encode('utf-8'))
    
    # packet 
    if serialInst.in_waiting:
        ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(dataList), interval=100)

        plt.show()


    
    # if command == 'exit':
    #     exit()



data = np.random.random((12,12))
plt.imshow(data)

plt.title("2-D Heat Map")
plt.show()
