import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

dataList = []
ser = serial.Serial("COM5", 9600)

fig = plt.figure()
ax = fig.add_subplot(111)

time.sleep(2)

def animate(i, dataList,ser):
    ser.write(b'g')
    arduinoData_String = ser.readline().decode('ascii')

    try:
        arduinoData_float = float(arduinoData_String)
        dataList.append(arduinoData_float)

    except:
        pass

    dataList = dataList[-50:]

    ax.clear()
    ax.plot(dataList)

    ax.set_ylim([0,5])
    ax.set_title("Arduino Data")
    ax.set_ylabel("Value")

 
ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(dataList,ser), interval=50)

plt.show()
ser.close()