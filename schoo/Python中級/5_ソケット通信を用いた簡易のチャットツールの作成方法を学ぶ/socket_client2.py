import socket

# クライアント側
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 50007))

your_input = input(">")
s.send(your_input.encode("utf-8"))

data = s.recv(1024)
print(repr(data))

s.close()
