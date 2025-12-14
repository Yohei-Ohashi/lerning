import socket
import threading  # 【追加】スレッド処理に必要なモジュール


# 【追加】接続しているすべてのクライアントを管理するリスト
# このリストに各クライアントのソケットを保存しておくことで、
# 後で「1つのクライアントからのメッセージを他の全クライアントに転送」できるようになる
clients: list[socket.socket] = []

# 【追加】複数のスレッドが同じリストにアクセスする際の競合を防ぐためのロック
# 例:2つのスレッドが同時にリストに追加しようとすると問題が起きる可能性があるため、
# ロックを使って「1つずつ順番に」処理するようにする
clients_lock = threading.Lock()


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
    # 【変更点2】 最大5つの接続を待機できるように変更
    server_socket.listen(5)
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

    # 【追加】このクライアントを管理リストに追加
    # with clients_lock: ロックを取得(他のスレッドがリストを変更できないようにする)
    # ロックを取得している間は、他のスレッドは待機する
    with clients_lock:
        clients.append(client_socket)
        print(f"[SERVER] 現在の接続数: {len(clients)}")

    try:
        while True:
            # 受信
            message = receive_message(client_socket)
            if message is None:
                break
            print(f"[CLIENT] {message}")

            # 送信
            input_text = input(">")
            send_message(client_socket, input_text)
    except Exception as e:
        # エラーが発生した場合(接続エラーなど)
        print(f"[SERVER] クライアント {client_address} でエラー: {e}")
    finally:
        # 【追加】クライアントが切断されたら、管理リストから削除
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
                print(f"[SERVER] クライアント {client_address} を切断しました")
                print(f"[SERVER] 現在の接続数: {len(clients)}")

        # クライアントソケットを閉じる
        client_socket.close()


def main():
    # サーバー側
    server_socket = create_server_socket()
    print("[SERVER] Waiting for connection...")
    print("[SERVER] 複数のクライアントが接続できます")

    try:
        # 【変更点1】無限ループを追加:新しいクライアントの接続を常に待ち続ける
        while True:
            # クライアントからの接続を待機し、接続を受け入れる
            client_socket, client_address = server_socket.accept()
            print(f"[SERVER] 新しいクライアントが接続しました: {client_address}")

            # 【追加】 新しいクライアントごとにスレッドを作成
            # threading.Thread: 新しいスレッドを作成するクラス
            # target: スレッド内で実行する関数を指定
            # args: その関数に渡す引数を指定(タプル形式)
            # daemon=True: メインプログラムが終了したら、このスレッドも自動的に終了
            client_thread = threading.Thread(
                target=handle_client,  # この関数をスレッド内で実行
                args=(client_socket, client_address),  # 関数に渡す引数
                daemon=True,  # バックグラウンドスレッドとして実行
            )

            # スレッドを開始:これで handle_client が別スレッドで実行される
            client_thread.start()

            # 重要: ここで Client_thread.join() を呼ばない理由
            # join() を呼ぶと、そのスレッドが終了するまで待つため、
            # 次のクライアントの接続を受け付けられなくなる
            # そのため、スレッドは「バックグラウンド」で実行させておく
    except KeyboardInterrupt:
        # Ctrl+Cで終了できるようにする
        print("\n[SERVER] サーバーを終了します...")
    finally:
        server_socket.close()
        print("[SERVER] サーバーソケットを閉じました")


if __name__ == "__main__":
    main()
