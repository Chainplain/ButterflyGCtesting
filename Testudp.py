import socket

def get_local_ip():
    try:
        # Create a socket and connect to a dummy address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))  # Doesn't need to be reachable
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'  # Fallback to localhost
    finally:
        s.close()
    return local_ip

# Get and print the local IP address
local_ip_address = get_local_ip()
print(f"Your local IP address is: {local_ip_address}")
