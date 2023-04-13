import socket
import threading

from socket_utils import receive_message,send_message,send_username,receive_username,exchange_keys

HOST = "127.0.0.1"
PORT = 12345  # Range 0 - 65538
LISTENER_LIMIT = 1


def main():
    # Creating Socket (tcp protocol)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Provide socket with an address in the form of Host IP and Port
        server.bind((HOST, PORT))
        print(f"Server Started ... host {HOST} and port {PORT}")
    except:
        print(f"Unable to binder to host {HOST} and port {PORT}")
    
    # Set Server Limit (Max no of clients)
    server.listen(LISTENER_LIMIT)

    # while 1:
    # Listening for client connection request
    client, address = server.accept()
    print(f"Connected to Client {address[0]} {address[1]} Successfully")

    # Exchange Keys
    e,d,n,n_client,e_client=exchange_keys(client)

    # print("your public key","e",e,"n",n,"d",d)
    
    # Send him your username
    username=input("Enter your username ")
    send_username(client,username,e_client,n_client)

    # Receive client username 
    print("Waiting for your friend 🚶‍♀️ .... ")
    client_username=receive_username(client,d,n)

    print(f"Started Chatting with {client_username} 🚀🚀")

    # Start a new thread to Receive messages
    threading.Thread(target=receive_message,args=(client,client_username,d,n)).start()

    # Send Message Using Current Thread
    send_message(client,e_client,n_client)

    

if __name__ == "__main__":
    main()
