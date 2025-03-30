import socket
import time
import subprocess
import platform
from datetime import datetime

def ping_host(host):
    """
    Returns True if host responds to ping
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def check_port(host, port):
    """
    Check if a port is open on a remote host
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            return s.connect_ex((host, port)) == 0
    except socket.error:
        return False

def network_latency(host):
    """
    Measure network latency to a host
    """
    try:
        start_time = time.time()
        socket.gethostbyname(host)
        end_time = time.time()
        return round((end_time - start_time) * 1000, 2)  # in milliseconds
    except socket.gaierror:
        return None

def monitor_network(devices, ports=[80, 443], interval=60):
    """
    Main monitoring function
    """
    print(f"Starting network monitoring at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    while True:
        for device in devices:
            print(f"\nChecking {device}...")
            
            # Ping check
            is_up = ping_host(device)
            status = "UP" if is_up else "DOWN"
            print(f"Status: {status}")
            
            if is_up:
                # Latency check
                latency = network_latency(device)
                if latency is not None:
                    print(f"Latency: {latency} ms")
                else:
                    print("Latency: Could not resolve host")
                
                # Port check
                for port in ports:
                    port_status = "OPEN" if check_port(device, port) else "CLOSED"
                    print(f"Port {port}: {port_status}")
            
            print("-"*40)
        
        print(f"\nMonitoring cycle completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Next check in {interval} seconds...")
        time.sleep(interval)

if __name__ == "__main__":
    # Configuration
    DEVICES_TO_MONITOR = ["google.com", "github.com", "localhost"]
    PORTS_TO_CHECK = [80, 443, 22]
    CHECK_INTERVAL = 300  # 5 minutes
    
    try:
        monitor_network(DEVICES_TO_MONITOR, PORTS_TO_CHECK, CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")