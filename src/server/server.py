import socket

HOST = "127.0.0.1"  # localhost - for now we run everything on the same machine
PORT = 5050         # port number used by the server


def run_server():
    # 1) Create a TCP socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) Bind the socket to IP + port
    server_sock.bind((HOST, PORT))

    # 3) Start listening for incoming connections
    server_sock.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    # 4) Wait until a client connects
    conn, addr = server_sock.accept()
    print(f"Connected by {addr}")

    # 5) Receive messages from the client and send them back (echo)
    while True:
        data = conn.recv(1024)  # receive up to 1024 bytes
        if not data:
            print("Client disconnected.")
            break

        message = data.decode("utf-8")
        print(f"Received from client: {message}")

        # echo: send the same data back to the client
        conn.sendall(data)

    conn.close()
    server_sock.close()


if __name__ == "__main__":
    run_server()