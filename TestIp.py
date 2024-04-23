import concurrent.futures
import socket

def scan_ip(ip):
    try:
        host_name = socket.gethostbyaddr(ip)[0]
        print(f"Found: {ip} - {host_name}")
    except socket.herror:
        print(f"Not found: {ip}")

def scan_local_network():
    prefix = '192.168.50.'
    ips = [prefix + str(i) for i in range(1, 256)]

    print("Scanning local network...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(scan_ip, ips)

if __name__ == "__main__":
    scan_local_network()
