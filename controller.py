from inputs import get_gamepad
import time
StartTime = time.time()
ElapsedTime = 15
now = time.time()

ABS_X_max_min = [0] * 2

ABS_Y_max_min = [0] * 2

ABS_Z_max_min = [0] * 2

ABS_RX_max_min  =  [0] * 2

ABS_RY_max_min  =  [0] * 2

ABS_RZ_max_min  =  [0] * 2


update_times = 0

def update_max_min(code, input, max_min_rec):
    global update_times
    if max_min_rec[0] < input:
        max_min_rec[0] = input
        update_times = update_times + 1
        print(code + ' update_times:', update_times)
    if max_min_rec[1] > input:
        max_min_rec[1] = input
        update_times = update_times + 1
        print(code+ ' update_times:', update_times)

while (now - StartTime) < ElapsedTime:
    events = get_gamepad()
    now = time.time()
    print(now - StartTime) 
    for event in events: 
        match event.code:
            case 'ABS_X': 
                update_max_min('ABS_X', event.state, ABS_X_max_min)
            case 'ABS_Y': 
                update_max_min('ABS_Y', event.state, ABS_Y_max_min)
            case 'ABS_Z': 
                update_max_min('ABS_Z', event.state, ABS_Z_max_min)
            case 'ABS_RX': 
                update_max_min('ABS_RX', event.state, ABS_RX_max_min)
            case 'ABS_RY': 
                update_max_min('ABS_RY', event.state, ABS_RY_max_min)
            case 'ABS_RZ': 
                update_max_min('ABS_RZ', event.state, ABS_RZ_max_min)
                
print('ABS_X', ABS_X_max_min[1], '->', ABS_X_max_min[0])
print('ABS_Y', ABS_Y_max_min[1], '->', ABS_Y_max_min[0])
print('ABS_Z', ABS_Z_max_min[1], '->', ABS_Z_max_min[0])
print('ABS_RX', ABS_RX_max_min[1], '->', ABS_RX_max_min[0])
print('ABS_RY', ABS_RY_max_min[1], '->', ABS_RY_max_min[0])
print('ABS_RZ', ABS_RZ_max_min[1], '->', ABS_RZ_max_min[0])