# server.py
import socket
from cryptography.fernet import Fernet 

# Generate and save a key for encryption/decryption
key = Fernet.generate_key()
cipher = Fernet(key)
print(f"Encryption Key: {key.decode()}")  # Share this with the client securely

def start_server(host='localhost', port=5555):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")
            with client_socket:
                # Receive encrypted message
                encrypted_message = client_socket.recv(1024)
                if encrypted_message:
                    # Decrypt the message
                    decrypted_message = cipher.decrypt(encrypted_message)
                    print(f"Received (decrypted): {decrypted_message.decode()}")
                else:
                    break

if __name__ == '__main__':
    start_server()
