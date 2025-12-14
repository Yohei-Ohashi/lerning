import socket

# サーバー側
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 50007))
s.listen(1)
client_socket, client_address = s.accept()

print(client_address)
data = client_socket.recv(1024)
print(repr(data))

your_input = input(">")
client_socket.send(your_input.encode("utf-8"))

#client_socket.sendall(data)

client_socket.close()
