import struct

def pack_bytes(category, data):
    frame_head = "UU"
    frame_head_bytes = frame_head.encode()
    
    cate_bytes = category.encode()
    
    data_no_bytes = bytes()
    data_bytes = bytes()
    check_sum_bytes = bytes()
    
    match category:
        case "S":
            data_no = len(data)
            data_no_bytes = data_no.to_bytes(1)
            data_bytes = data.encode()
            check_sum = 0
            for datum in data:
                print(ord(datum))
                check_sum = check_sum + ord(datum)
                
            check_sum = check_sum & 0xFF
            check_sum_bytes = check_sum.to_bytes(1)
    
        case "F":
            data_no = len(data) * 4
            data_no_bytes = data_no.to_bytes(1)
            for datum in data:
                data_bytes = data_bytes + struct.pack('f', datum)
            check_sum = 0
            for d_byte_int in data_bytes:
                check_sum = check_sum + d_byte_int
            check_sum = check_sum & 0xFF
            check_sum_bytes = check_sum.to_bytes(1)
                
    send_bytes = frame_head_bytes + cate_bytes +  data_no_bytes + data_bytes + check_sum_bytes
    return send_bytes

print(pack_bytes("S","AA"))

print(pack_bytes("F",[0.1231,0,0,0]))   