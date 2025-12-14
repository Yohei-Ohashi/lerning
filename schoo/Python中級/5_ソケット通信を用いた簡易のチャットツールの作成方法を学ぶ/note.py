import socket

# クライアント側
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IPアドレス: 127.0.0.1, ポート番号: 50007に接続します
s.connect(("127.0.0.1", 50007))

s.sendall(b"Hello, World")
data = s.recv(1024)
print("Received from server:", repr(data))

s.close()
