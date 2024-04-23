import serial
import struct
import csv
import numpy as np
from datetime import datetime
from datetime import date
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import time
import _thread

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('ADC showing 1 and 2')
win.setBackground((254,254,248))

# 3) Plot in chunks, adding one new plot curve1 for every 100 samples
chunkSize = 100
# Remove chunks after we have 10
maxChunks = 100
startTime = time.time()
win.nextRow()
p_adc_1 = win.addPlot(colspan=2)
p_adc_1.setLabel('bottom', 'Time', 's') 
p_adc_1.setLabel('top', 'ADC 1')
p_adc_1.setXRange(-10, 0)
win.nextRow()
p_adc_2 = win.addPlot(colspan=2)
p_adc_2.setLabel('bottom', 'Time', 's')
p_adc_2.setLabel('top', 'ADC 2')
p_adc_2.setXRange(-10, 0)

plot_ptr = 0
curve1s = []
data_1 = np.zeros((chunkSize + 1, 2))
adc_1_float = 0.0

curve2s = []
data_2 = np.zeros((chunkSize + 1, 2))
adc_2_float = 0.0

def update_plot():
    global plot_ptr, p_adc_1, data_1, curve1s, adc_1_float,\
                     p_adc_2, data_2, curve2s, adc_2_float, chunkSize, maxChunks
    now = time.time()
    for c in curve1s:
        c.setPos(-(now - startTime), 0)
        
    for c2 in curve2s:
        c2.setPos(-(now - startTime), 0)

    i = plot_ptr % chunkSize
    if i == 0:
        penhere = pg.mkPen(color=(150,100,0), width=2)
        curve1 = p_adc_1.plot(pen=penhere)
        curve1s.append(curve1)
        last1 = data_1[-1]
        data_1 = np.empty((chunkSize + 1, 2))
        data_1[0] = last1
        while len(curve1s) > maxChunks:
            c = curve1s.pop(0)
            p_adc_1.removeItem(c)
        
        penhere2 = pg.mkPen(color=(100,0,150), width=2)
        curve2 = p_adc_2.plot(pen=penhere2)
        curve2s.append(curve2)
        last2 = data_2[-1]
        data_2 = np.empty((chunkSize + 1, 2))
        data_2[0] = last2
        while len(curve2s) > maxChunks:
            c2 = curve2s.pop(0)
            p_adc_2.removeItem(c2)
    else:
        if len(curve1s) > 0:
            curve1 = curve1s[-1]
            curve2 = curve2s[-1]
    data_1[i + 1, 0] = now - startTime
    data_1[i + 1, 1] = adc_1_float
    curve1.setData(x=data_1[:i + 2, 0], y=data_1[:i + 2, 1])
    
    data_2[i + 1, 0] = now - startTime
    data_2[i + 1, 1] = adc_2_float
    curve2.setData(x=data_2[:i + 2, 0], y=data_2[:i + 2, 1])
    plot_ptr += 1
    
# import os





start_time = time. time()


def recording_thread():
    global adc_1_float, adc_2_float
    ser = serial.Serial('COM3', 600000)  # Replace 'COM1' with the appropriate port name and 9600 with the desired baud rate
    Frame_data = ""
    read_length = 1000
    Frame_read_complete = True
    Frame_data_count = 0
    Info_data_count = 0
    Record_time_length = 10# in seconds
    current_day = date.today().strftime("_%Y_%m_%d_")
    current_time = datetime.now().strftime("%I_%M_%S_%p")

    File_name = "data/serialdiradcVal" +current_day + current_time +".csv"

    Record = []
    while ( time. time() - start_time ) < Record_time_length:
        try:
                data = ser.read(read_length)
                # print(data)
                
                for datum in data:
                    if datum == 85 and Frame_read_complete and Frame_data_count == 0: # first byte 0x55
                        Frame_read_complete = False
                        Frame_data_count = Frame_data_count + 1
                        Frame_data = []
                        continue
                        # print('Frame got!')
                    if datum == 85 and (not Frame_read_complete) and Frame_data_count == 1: # second byte 0x55
                        Frame_data_count = Frame_data_count + 1
                        continue
                    if Frame_data_count == 2 and (not Frame_read_complete) and datum == 115: # third byte 's'
                        Frame_data_count = Frame_data_count + 1
                        continue
                    if Frame_data_count == 3 and (not Frame_read_complete): # third byte 's'
                        Frame_data_count = Frame_data_count + 1
                        Info_data_count = datum
                        continue
                    if Frame_data_count == 4 and Info_data_count>0 and (not Frame_read_complete):
                        Info_data_count = Info_data_count - 1
                        Frame_data.append(datum) 
                        continue
                    # print(Frame_data)
                    if len(Frame_data)== 224:
                        read_ptr = 0
                        # print(Frame_data)                  
                        for i in range(20):
                            Frame = [0.0] * 2
                            int_values = Frame_data[read_ptr:read_ptr + 4]
                            binary_data = struct.pack('4B', *int_values)
                            float_value = struct.unpack('f', binary_data)[0]
                            Frame[0] = float_value
                            int_values = Frame_data[read_ptr + 4 * 20:read_ptr + 4 + 4 * 20]
                            binary_data = struct.pack('4B', *int_values)
                            float_value = struct.unpack('f', binary_data)[0]
                            Frame[1] = float_value
                            read_ptr = read_ptr + 4
                            Record.append(Frame)
                        # os.system('cls' if os.name == 'nt' else 'clear')
                        # print("ADC2: ",Frame[1])
                        adc_1_float = Frame[0]
                        adc_2_float = Frame[1]
                        # print(adc_Frame)
                    # IF all the cases are not triggered.
                    Frame_data_count = 0
                    Frame_read_complete = True
                    Info_data_count = 0
                    Frame_data = []        
        except KeyboardInterrupt:
            pass
        
        
    with open(File_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(Record)
        

    ser.close()

timer = pg.QtCore.QTimer()
timer.timeout.connect(update_plot)
timer.start(50)

_thread.start_new_thread(recording_thread, ())
time.sleep(0.2)



QtGui.QGuiApplication.instance().exec_()
