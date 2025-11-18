import socket

HOST = "127.0.0.1"  # server ip'si (simdilik ayni makine)
PORT = 5050         # server'in dinledigi port


def run_client():
    # 1) TCP socket olustur
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) Server'a baglan
    sock.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    try:
        while True:
            # kullanicidan input al
            message = input("You: ")

            # cikis komutlari
            if message.lower() in ("q", "quit", "exit"):
                print("Exiting client...")
                break

            # mesaji byte'a cevir ve gonder
            sock.sendall(message.encode("utf-8"))

            # server'dan cevap bekle
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