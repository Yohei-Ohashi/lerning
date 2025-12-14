import socket

# サーバー側
server_socket = socket.socket()
# IPアドレス: 127.0.0.1, ポート番号: 50007で待ちます
server_socket.bind(("127.0.0.1", 50007))
# 1人来たら次は待たせる
server_socket.listen(1)
client_socket, client_address = server_socket.accept()
print("Connected by", client_address)

# ループで通信（エコーサーバー）
while True:
    # クライアントからのデータを受信
    data = client_socket.recv(1024)
    if not data:
        break
    # 受信したデータを表示
    print("Received", repr(data))
    # 受信したデータをそのままクライアントに送り返す(エコー)
    client_socket.sendall(data)

client_socket.close()
