Framehead = "UU".encode()
Heart_beat_text = "HB"
Length = len(Heart_beat_text)
sum = 0 
for alpha in Heart_beat_text:
    sum += ord(alpha)
check = sum & 0xFF
print('check: ',check)
checkbyte = check.to_bytes(1,'big')
print('checkbyte: ',checkbyte)
data = Framehead + Length.to_bytes(1,'big') + Heart_beat_text.encode() + checkbyte
print(data)