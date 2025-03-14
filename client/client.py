import socket
import ssl

def echo_client(server_host='127.0.0.1', server_port=8443, certfile='./certs/server.crt'):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(certfile)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        secure_socket = context.wrap_socket(client_socket, server_hostname=server_host)
        secure_socket.connect((server_host, server_port))
        print("Connected to server with SSL")
        try:
            while True:
                message = input("Enter message (or type 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Exiting")
                    break
                secure_socket.sendall(message.encode())
                data = secure_socket.recv(1024)
                print(f"Received from server: {data.decode()}")
        except Exception as e:
            print("Error:", e)
        finally:
            secure_socket.close()
            print("Closing connection.")

if __name__ == "__main__":
    echo_client()
