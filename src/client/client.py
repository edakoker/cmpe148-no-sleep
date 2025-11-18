import socket

HOST = "127.0.0.1"  # server IP (for now, same machine)
PORT = 5050         # port where the server is listening


def run_client():
    # 1) Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) Connect to the server
    sock.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    try:
        while True:
            # read user input from the terminal
            message = input("You: ")

            # exit commands
            if message.lower() in ("q", "quit", "exit"):
                print("Exiting client...")
                break

            # convert text to bytes and send it to the server
            sock.sendall(message.encode("utf-8"))

            # wait for a reply from the server
            data = sock.recv(1024)
            if not data:
                print("Server closed the connection.")
                break

            reply = data.decode("utf-8")
            print(f"Server echoed: {reply}")
    finally:
        sock.close()


if __name__ == "__main__":
    run_client()