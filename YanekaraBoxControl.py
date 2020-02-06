import serial
import time
import threading
import sys

def func1():
    while True:
        #if quit == True:
        #    sys.exit()
        try:
            ser = serial.Serial("/dev/ttyUSB0", 115200,
                dsrdtr = True,timeout=None,writeTimeout=None)
            line = ser.readline()
            file = open('result.txt','a')
            file.write(line)
            file.close()
            ser.close()
        except serial.SerialException:
            continue

def SerialWrite(Index):
    ser = serial.Serial("/dev/ttyUSB0",115200,
    dsrdtr = True, timeout=None, writeTimeout=None)
    ser.write(b'{}'.format(Index))
    ser.close()

def SystemControl(order,Autonomous):
    if order=="3":
        SerialWrite(3)
        if Autonomous[0]: 
            Autonomous[0] = False
        else:
            Autonomous[0] = True
    elif order=="4":
        print("Ending The System")
        sys.exit()
    else:
        print("incorrectNumber!")


def func2():
    Autonomous = [True]
    while True:
        try:
            if Autonomous[0]:
                print("Autonomous Mode")
                print("[3] Switch   [4]endSystem")
                order = raw_input()
                SystemControl(order,Autonomous) 
            else:
                print("[0]Stop   [1]Charge   [2]Discharge")
                print("[3] Switch   [4]endSystem")
		order = raw_input()
                if order == "0":
                    SerialWrite(0)
                elif order == "1":
                    SerialWrite(1)
                elif order == "2":
                    SerialWrite(2)
                else:
		    SystemControl(order,Autonomous)
        except EOFError:
            continue

if __name__ == "__main__":
    thread_1 = threading.Thread(target=func1)
    thread_1.setDaemon(True)
    thread_2 = threading.Thread(target=func2)

    thread_1.start()
    thread_2.start()
