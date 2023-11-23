import serial
import struct
import csv
import numpy as np
from datetime import datetime
from datetime import date
import time

ser = serial.Serial('COM3', 115200)  # Replace 'COM1' with the appropriate port name and 9600 with the desired baud rate
Frame_data = ""
read_length = 100
Frame_read_complete = True
Frame_data_count = 0
Info_data_count = 0

Record_time_length = 10
current_day = date.today().strftime("_%Y_%m_%d_")
current_time = datetime.now().strftime("%I_%M_%S_%p")

File_name = "pureadcVal" +current_day + current_time +".csv"

adc_record = []

start_time = time. time()

while True:
    try:
            data = ser.read(read_length)
            # print(data)
            
            for datum in data:
                if datum == 85 and Frame_read_complete and Frame_data_count == 0: # first byte 0x55
                    Frame_read_complete = False
                    Frame_data_count = Frame_data_count + 1
                    Frame_data = ""
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
                    Frame_data = Frame_data + chr(datum)
                    continue
                # print(Frame_data)
                if len(Frame_data)==72:
                    read_ptr = 0
                    adc_Frame = [0.0] * 9
                    for i in range(9):
                        buff = Frame_data[read_ptr:read_ptr + 8]
                        read_ptr = read_ptr + 8
                        temp_float = struct.unpack('<f', bytes.fromhex(buff))[0]
                        adc_Frame[i] = temp_float
                            # print(temp_float)
                        # temp_uint16 = int(buff, 16)
                        # print(temp_uint16)
                    # print('_________________')
                    adc_record.append(adc_Frame)
                # IF all the cases are not triggered.
                Frame_data_count = 0
                Frame_read_complete = True
                Info_data_count = 0        
    except KeyboardInterrupt:
        pass
    
    if ( time. time() - start_time ) > Record_time_length:
        break
    
with open(File_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(adc_record)
    

ser.close()