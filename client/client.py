import socket

def echo_client(server_host='127.0.0.1', server_port=1234):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        print("Connected to echo server on {}:{}".format(server_host, server_port))
        try:
            while True:
                message = input("Enter message (or type 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Exiting.")
                    break
                # Send the message to the server
                client_socket.sendall(message.encode())
                # Wait for the echoed response from the server
                data = client_socket.recv(1024)
                print("Echoed from server:", data.decode())
        except Exception as e:
            print("Error:", e)
        finally:
            print("Closing connection.")

if __name__ == "__main__":
    echo_client()
