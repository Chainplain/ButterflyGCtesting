import socket
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
import threading
import select

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('ESP ADC showing 1 and 2')
win.setBackground((254,254,248))

time_length_has_not_rec_data_in_sec = 0.0

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

loses_count = 0

single_try = True


def is_socket_closed(sock):
    global time_length_has_not_rec_data_in_sec, loses_count
    max_time_length_has_not_rec_data_in_sec = 3
    if sock and (time_length_has_not_rec_data_in_sec <= max_time_length_has_not_rec_data_in_sec):
        return False
        # try:
        #     # Use fileno() method to get the socket file descriptor
        #     fileno = sock.fileno()
        #     _, writable, _ = select.select([], [sock], [], 0)
        #     return fileno not in writable
        # except Exception as e:
        #     return True
    else:
        loses_count = loses_count + 1
        print("Client loses:", loses_count)
        return True
    
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

mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '192.168.50.141'  # Use your desired IP address or hostname
port = 6001  # Use your desired port number
# server_socket.settimeout(3)
try:
    mysocket.bind((host, port))
    # server_socket.listen()
    # client_socket, client_address = server_socket.accept()
    # client_socket.settimeout(5)
except Exception as e:
    pass


TCP_write_thread = threading.Lock()
Socket_connect_thread = threading.Lock()



    
def send_heart_beat():
    global mysocket, time_length_has_not_rec_data_in_sec,single_try,host, port
    hear_beat_period = 0.5
    while(True):
        time.sleep(hear_beat_period)
        TCP_write_thread.acquire()
        time_length_has_not_rec_data_in_sec = time_length_has_not_rec_data_in_sec + hear_beat_period
        try:
                data = b'Hello, server!'
                sendhost = '192.168.50.143'
                sendport = 6101
                mysocket.sendto(data, (sendhost, sendport))


        finally:
            TCP_write_thread.release()

            
def recording_thread():
    global adc_1_float, adc_2_float, single_try
    global mysocket, time_length_has_not_rec_data_in_sec,host, port
    Frame_data = ""
    read_length = 10000
    Frame_read_complete = True
    Frame_data_count = 0
    Info_data_count = 0
    Record_time_length = 10# in seconds
    current_day = date.today().strftime("_%Y_%m_%d_")
    current_time = datetime.now().strftime("%I_%M_%S_%p")

    File_name = "data/diradcVal" +current_day + current_time +".csv"
    single_try = True
    
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 6001  # Use your desired port number
    mysocket.bind(("",6001))
    # mysocket.settimeout(0.1)
    
    Record = []
    start_time = time. time()
    check_num = 0
    ischecked = False
    
    while ( time. time() - start_time ) < Record_time_length:
        # print('Time:',time. time() )
        # if (not is_socket_closed(mysocket)) or single_try:
            data = mysocket.recv(read_length)
            for datum in data:
                if datum == 85 and Frame_read_complete and Frame_data_count == 0: # first byte 0x55
                    Frame_read_complete = False
                    Frame_data_count = Frame_data_count + 1
                    Frame_data = []
                    continue
                    # print('Frame got!')
                if datum == 85 and (not Frame_read_complete) and Frame_data_count == 1: # second byte 0x55
                    Frame_data_count = Frame_data_count + 1
                    time_length_has_not_rec_data_in_sec = 0.0
                    continue
                if Frame_data_count == 2 and (not Frame_read_complete) and datum == 115: # third byte 's'
                    Frame_data_count = Frame_data_count + 1
                    continue
                if Frame_data_count == 3 and (not Frame_read_complete): # third byte 's'
                    Frame_data_count = Frame_data_count + 1
                    Info_data_count = datum
                    ischecked = False
                    check_num = 0
                    continue
                
                if Frame_data_count == 4 and Info_data_count > 0 and (not Frame_read_complete):
                    Info_data_count = Info_data_count - 1
                    Frame_data.append(datum)
                    check_num = check_num +  datum
                    continue
                
                if Frame_data_count == 4 and Info_data_count == 0 and (not Frame_read_complete):
                    ischecked = (datum == check_num & 0xFF)
                    
                
                # print(Frame_data)
                if  len(Frame_data)== 232 and ischecked:
                    read_ptr = 8
                    # print(Frame_data) 
                    FramesInaRead=20                 
                    for i in range(FramesInaRead):
                        Frame = [0.0] * 2
                        int_values = Frame_data[read_ptr:read_ptr + 4]
                        binary_data = struct.pack('4B', *int_values)
                        float_value = struct.unpack('f', binary_data)[0]
                        Frame[0] = float_value
                        int_values = Frame_data[read_ptr + 4 * FramesInaRead:read_ptr + 4 + 4 * FramesInaRead]
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
            
    with open(File_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(Record)
        

    # client_socket.close()
    # server_socket.close()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update_plot)
timer.start(50)

data = b'Hello, server!'
sendhost = '192.168.50.143'
sendport = 6101
mysocket.sendto(data, (sendhost, sendport))

_thread.start_new_thread(recording_thread,())
_thread.start_new_thread(send_heart_beat, ())
# _thread.start_new_thread(send_heart_beat2, ())
# record_th = threading.Thread(target=recording_thread)
# record_th.start()

time.sleep(0.2)



QtGui.QGuiApplication.instance().exec_()
# record_th.join()