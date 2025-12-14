"""
チャットツール開発課題 - サーバー側プログラム

【基本要件】
以下の4つのステップを繰り返し実行できるチャットツールを作成してください。

ステップ1: クライアントからサーバーへのメッセージ送信
    - クライアント側が任意のメッセージをサーバーに送信します
    - （このステップはクライアント側で実装します）

ステップ2: サーバー側でメッセージを受信してコンソールに表示
    - クライアントから送信されたメッセージを受信します
    - 受信したメッセージをサーバーのコンソールに表示します
    - 実装箇所: このファイル（server.py）で実装してください

ステップ3: サーバーからクライアントへのメッセージ送信
    - サーバー側が任意のメッセージをクライアントに送信します
    - 実装箇所: このファイル（server.py）で実装してください

ステップ4: クライアント側でメッセージを受信してコンソールに表示
    - クライアント側でサーバーからのメッセージを受信して表示します
    - （このステップはクライアント側で実装します）

【実装のポイント】
- ソケット通信を使用してクライアントと接続します
- 上記のステップ2とステップ3を繰り返し実行できるようにループ処理を実装してください
- メッセージの送受信は適切なエンコーディング（UTF-8など）を使用してください
- 接続が切断された場合の処理も考慮してください

【オプション課題（時間があれば）】
- スレッド処理を使用して、複数のクライアントと同時に通信できるようにしてください
- 複数のクライアントが接続できるように、各クライアントごとにスレッドを作成して処理を分離してください
- 1つのクライアントからのメッセージを、接続している他のすべてのクライアントに転送する機能を実装してください

【参考】
- 既存のサンプルコード: schoo/Python中級/5_ソケット通信を用いた簡易のチャットツールの作成方法を学ぶ/socket_server.py
- 既存のサンプルコード: schoo/Python中級/5_ソケット通信を用いた簡易のチャットツールの作成方法を学ぶ/socket_server2.py
"""

# TODO: ここから実装を開始してください
# 1. 必要なモジュールをインポート（socketモジュールなど）
# 2. ソケットを作成して、IPアドレスとポート番号を指定してバインド
# 3. クライアントからの接続を待機（listen）
# 4. クライアントが接続したら、接続を受け入れる（accept）
# 5. ループ処理で以下を繰り返し実行:
#    a. クライアントからのメッセージを受信（recv）
#    b. 受信したメッセージをコンソールに表示（print）
#    c. サーバー側から任意のメッセージをクライアントに送信（send/sendall）
# 6. 接続が終了したら、ソケットを閉じる（close）

# 【オプション課題用のメモ】
# - threadingモジュールを使用して、各クライアントごとにスレッドを作成
# - 複数のクライアント接続を管理するためのリストや辞書を使用
# - 各スレッド内でクライアントとの通信を処理

import socket


def create_server_socket(host: str = "127.0.0.1", port: int = 50007) -> socket.socket:
    """
    サーバーソケットを作成し、指定されたホストとポートにバインドします。

    引数:
        host (str): サーバーのIPアドレス（デフォルト: 127.0.0.1）
        port (int): サーバーのポート番号（デフォルト: 50007）

    戻り値:
        socket: 作成されたサーバーソケット
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    return server_socket


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


def handle_client(
    client_socket: socket.socket, client_address: tuple[str, int]
) -> None:
    """
    クライアントとの通信を処理します。
    メッセージの受信と送信を繰り返し実行します。

    Args:
        client_socket (socket): クライアントとの接続ソケット
        client_address (tuple): クライアントのアドレス情報
    """
    print(f"[SERVER] クライアント接続確認:{client_address}")

    while True:
        # 受信
        message = receive_message(client_socket)
        if message is None:
            break
        print(f"[CLIENT] {message}")

        # 送信
        input_text = input(">")
        send_message(client_socket, input_text)


def main():
    # サーバー側
    server_socket = create_server_socket()
    print("[SERVER] Waiting for connection...")

    try:
        # クライアントからの接続を待機し、接続を受け入れる
        client_socket, client_address = server_socket.accept()

        try:
            handle_client(client_socket, client_address)
        finally:
            # クライアントソケットを閉じる(接続を終了)
            client_socket.close()
            print("[SERVER] クライアントソケットを閉じました")
    finally:
        server_socket.close()
        print("[SERVER] サーバーソケットを閉じました")


if __name__ == "__main__":
    main()
