
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = "0.0.0.0"   # Accept connections from any device
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address} has connected.")

        client.send(
            bytes(
                "Welcome to the Chat Room!\nEnter your name:",
                "utf8"
            )
        )

        addresses[client] = client_address

        Thread(
            target=handle_client,
            args=(client,)
        ).start()

def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")

    welcome = f"Welcome {name}! Type {{quit}} to exit."
    client.send(bytes(welcome, "utf8"))

    msg = f"{name} has joined the chat!"
    broadcast(bytes(msg, "utf8"))

    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)

        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()

            del clients[client]

            broadcast(
                bytes(
                    f"{name} has left the chat.",
                    "utf8"
                )
            )
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Server started.")
    print("Waiting for connections...")

    ACCEPT_THREAD = Thread(
        target=accept_incoming_connections
    )

    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()

    SERVER.close() 