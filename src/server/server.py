import socket

HOST = "127.0.0.1"  # localhost - simdilik kendi bilgisayarimiz
PORT = 5050         # kullanacagimiz port numarasi


def run_server():
    # 1) TCP socket olustur
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) IP + port'a bagla
    server_sock.bind((HOST, PORT))

    # 3) Dinlemeye basla
    server_sock.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    # 4) Bir client baglanana kadar bekle
    conn, addr = server_sock.accept()
    print(f"Connected by {addr}")

    # 5) Client'tan mesaj al ve geri gonder (echo)
    while True:
        data = conn.recv(1024)  # max 1024 byte al
        if not data:
            print("Client disconnected.")
            break

        message = data.decode("utf-8")
        print(f"Received from client: {message}")

        # gelen mesaji aynen geri gonder
        conn.sendall(data)

    conn.close()
    server_sock.close()


if __name__ == "__main__":
    run_server()