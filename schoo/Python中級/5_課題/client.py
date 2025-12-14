import socket

# クライアント側
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 50007))

while True:
    input_text = input(">")
    # quitで終了させる
    if input_text == "quit":
        print("「quit」が入力されたので終了します。")
        break
    client_socket.send(input_text.encode("utf-8"))

    data_byte = client_socket.recv(1024)
    if not data_byte:
        break
    data_text = data_byte.decode("utf-8")
    print(f"[SERVER] {data_text}")

client_socket.close()
