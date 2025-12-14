import socket


def create_client_socket(host: str = "127.0.0.1", port: int = 50007) -> socket.socket:
    """
    クライアントソケットを作成し、指定されたホストとポートに接続します。

    Args:
        host (str): サーバーのIPアドレス（デフォルト: 127.0.0.1）
        port (int): サーバーのポート番号（デフォルト: 50007）

    Returns:
        socket.socket: 作成されたクライアントソケット
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket


def receive_message(client_socket: socket.socket) -> str | None:
    """クライアントからメッセージを受信する

    Args:
        client_socket (socket.socket): クライアントとの接続ソケット

    Returns:
        str | None: 受信したメッセージ文字列。接続が切断された場合はNone
    """
    data_byte = client_socket.recv(1024)
    if not data_byte:
        return None
    return data_byte.decode("utf-8")


def send_message(client_socket: socket.socket, message: str):
    """クライアントにメッセージを送信する

    Args:
        client_socket (socket.socket): クライアントとの接続ソケット
        message (str): 送信するメッセージ文字列
    """
    client_socket.send(message.encode("utf-8"))


def handle_server(client_socket: socket.socket):

    while True:
        input_text = input(">")
        # quitで終了させる
        if input_text == "quit":
            print("「quit」が入力されたので終了します。")
            break
        send_message(client_socket, input_text)

        message = receive_message(client_socket)
        if message is None:
            break
        print(f"[SERVER] {message}")


def main():
    # クライアント側
    client_socket = create_client_socket()

    try:
        handle_server(client_socket)
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
