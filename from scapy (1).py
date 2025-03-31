from scapy.all import sniff, IP, ICMP

# Specify the target IP for google.com (you can also ping it directly to confirm IP)
TARGET_IP = "8.8.8.8"

def detect_ping(packet):
    # Check if the packet is an ICMP (ping) request going to google.com IP
    if packet.haslayer(IP) and packet[IP].dst == TARGET_IP and packet.haslayer(ICMP):
        print("Detected a ping to google.com!")

# Start sniffing for ICMP packets
print("Listening for pings to google.com...")
sniff(filter="icmp", prn=detect_ping, store=0)
