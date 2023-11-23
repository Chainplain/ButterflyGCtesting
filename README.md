# ButterflyGCtesting

Require possible pip installs:
```
pip install pyserial
pip install pyqtgraph
pip install pyQT5
```

If you want to record something run adc2_dir_read.py directly.

- Check and use the correct serial port name:
``` python
ser = serial.Serial('COM3', 600000)
```

- Check and use the recod length:
``` python
Record_time_length = 30# in seconds
```
