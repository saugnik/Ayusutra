import socket
import time
import sys

start_time = time.time()
while time.time() - start_time < 30:
    try:
        with socket.create_connection(("localhost", 8001), timeout=1):
            print("Port 8001 is open!")
            sys.exit(0)
    except (ConnectionRefusedError, socket.timeout):
        time.sleep(1)

print("Timeout waiting for port 8001")
sys.exit(1)
