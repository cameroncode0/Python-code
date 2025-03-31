import ipaddress

class IPList:
    def __init__(self):
        self.ip_list = []

    def add_ip(self, ip):
        try:
            # Validate IP address
            ipaddress.ip_address(ip)
            self.ip_list.append(ip)
            print(f"IP address {ip} added.")
        except ValueError:
            print(f"Invalid IP address: {ip}")

    def remove_ip(self, ip):
        try:
            self.ip_list.remove(ip)
            print(f"IP address {ip} removed.")
        except ValueError:
            print(f"IP address {ip} not found in the list.")

    def display_ips(self):
        if self.ip_list:
            print("IP List:")
            for ip in self.ip_list:
                print(ip)
        else:
            print("The IP list is empty.")

    def ip_exists(self, ip):
        return ip in self.ip_list

# Example usage:
ip_manager = IPList()
ip_manager.add_ip("192.168.1.1")
ip_manager.add_ip("256.256.256.256")  # Invalid IP
ip_manager.display_ips()
print("Does 192.168.1.1 exist?", ip_manager.ip_exists("192.168.1.1"))
ip_manager.remove_ip("192.168.1.1")
ip_manager.display_ips()
#display_ips
