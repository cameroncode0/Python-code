import scapy.all as scapy
import tkinter as tk
from tkinter import ttk, messagebox
import socket
import os
import re
import csv
import requests

# Function to detect the local network range
def get_local_network():
    try:
        if os.name == "nt":  # Windows
            output = os.popen("ipconfig").read()
            match = re.search(r"IPv4 Address[^\d]*(\d+\.\d+\.\d+)\.\d+", output)
        else:  # Mac/Linux
            output = os.popen("ifconfig" if os.system("ifconfig > /dev/null 2>&1") == 0 else "ip -4 addr").read()
            match = re.search(r"inet (\d+\.\d+\.\d+)\.\d+", output)

        if match:
            return f"{match.group(1)}.1/24"  # Construct network range
    except Exception as e:
        print(f"ERROR: {e}")
        return None
    return None

# Function to get manufacturer details from MAC address
def get_mac_vendor(mac_address):
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
    except:
        pass
    return "Unknown"

# Function to scan the network
def scan(ip_range):
    devices = []
    try:
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        for sent, received in answered_list:
            try:
                hostname = socket.gethostbyaddr(received.psrc)[0]  # Get device name
            except socket.herror:
                hostname = "Unknown"

            vendor = get_mac_vendor(received.hwsrc)  # Get manufacturer
            devices.append({"IP": received.psrc, "MAC": received.hwsrc, "Name": hostname, "Vendor": vendor})
    except Exception as e:
        print(f"ERROR: Failed to scan network. {e}")
    return devices

# Function to display the results in GUI
def display_results():
    network = get_local_network()
    if not network:
        status_label.config(text="ERROR: Network not detected!", fg="red")
        return

    status_label.config(text=f"Scanning {network} ...", fg="blue")
    root.update()

    results = scan(network)

    for item in tree.get_children():
        tree.delete(item)

    if not results:
        status_label.config(text="No devices found!", fg="red")
        return

    for device in results:
        tree.insert("", "end", values=(device["IP"], device["MAC"], device["Name"], device["Vendor"]))

    status_label.config(text="Scan Complete!", fg="green")

# Function to export results to CSV
def export_to_csv():
    results = []
    for item in tree.get_children():
        results.append(tree.item(item)["values"])

    if not results:
        messagebox.showwarning("No Data", "No scan results to save!")
        return

    with open("network_scan_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP Address", "MAC Address", "Device Name", "Vendor"])
        writer.writerows(results)

    messagebox.showinfo("Export Successful", "Scan results saved to 'network_scan_results.csv'!")

# GUI Setup
root = tk.Tk()
root.title("Advanced Network Scanner")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

scan_button = tk.Button(frame, text="Scan My Network", command=display_results)
scan_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(frame, text="Export to CSV", command=export_to_csv)
export_button.pack(side=tk.LEFT, padx=5)

status_label = tk.Label(root, text="Scanning network, please wait...", fg="blue")
status_label.pack(pady=5)

columns = ("IP", "MAC", "Name", "Vendor")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("IP", text="IP Address")
tree.heading("MAC", text="MAC Address")
tree.heading("Name", text="Device Name")
tree.heading("Vendor", text="Manufacturer")

tree.pack(pady=10, fill="both", expand=True)

# **Auto-run the scan when the file is opened**
root.after(1000, display_results)  # Runs after 1 second

root.mainloop()
