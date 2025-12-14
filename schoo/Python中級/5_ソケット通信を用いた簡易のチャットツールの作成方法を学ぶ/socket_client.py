import socket

# クライアント側
client_socket = socket.socket()
# IPアドレス: 127.0.0.1, ポート番号: 50007に接続します
client_socket.connect(("127.0.0.1", 50007))

# サーバーに送信
client_socket.sendall(b"Hello, World")
# サーバーからの応答を受信(待機)
data = client_socket.recv(1024)
# 受信したデータを表示
print("Received from server:", repr(data))

client_socket.close()
