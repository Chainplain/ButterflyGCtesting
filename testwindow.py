import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import time
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('pyqtgraph example: Scrolling Plots')
win.setBackground((254,254,248))

# 3) Plot in chunks, adding one new plot curve for every 100 samples
chunkSize = 100
# Remove chunks after we have 10
maxChunks = 10
startTime = time.time()


class plot_mannager:
    def __init__(self, fatherWindow, topname, data_dim, leftlabel = 'rad'):
        self. plotcurve = fatherWindow.addPlot(colspan=2)
        self. plotcurve.setLabel('bottom', 'Time', 's')
        self. plotcurve.setLabel('top', topname)
        self. plotcurve.setLabel('left', leftlabel)
        self. plotcurve.setXRange(-10, 0)
        self. dim = data_dim
        self. chunkSize = 100
        self. maxChunks = 100
        self. curves = []
        self.Color_list = []
        self.Color_list.append((100,100,100))
        self.Color_list.append((255,150,150))
        self.Color_list.append((100,200,100))
        self.Color_list.append((150,150,255))
        
    def update_plot(self, datum_in_this_frame):
        now = time.time()
        for c in self. curves:
            c.setPos(-(now - startTime), 0)
        
        
p_adc_1 = plot_mannager(win)
win.nextRow()

p_adc_2 = win.addPlot(colspan=2)
p_adc_2.setLabel('bottom', 'Time', 's')
p_adc_2.setXRange(-10, 0)

curves = []
data_1 = np.empty((chunkSize + 1, 2))
ptr5 = 0



def update_plot():
    global p_adc_1, data_1, ptr5, curves
    now = time.time()
    for c in curves:
        c.setPos(-(now - startTime), 0)

    i = ptr5 % chunkSize
    if i == 0:
        penhere = pg.mkPen(color=(100,100,100), width=2)
        curve = p_adc_1.plotcurve.plot(pen=penhere)
        curves.append(curve)
        last = data_1[-1]
        data_1 = np.empty((chunkSize + 1, 2))
        data_1[0] = last
        while len(curves) > maxChunks:
            c = curves.pop(0)
            p_adc_1.plotcurve.removeItem(c)
    else:
        curve = curves[-1]
    data_1[i + 1, 0] = now - startTime
    data_1[i + 1, 1] = np.random.normal()
    curve.setData(x=data_1[:i + 2, 0], y=data_1[:i + 2, 1])
    ptr5 += 1


# update all plots
def update():
    update_plot()
    
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    QtGui.QGuiApplication.instance().exec_()
