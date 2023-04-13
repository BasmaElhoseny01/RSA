import socket
import threading

from socket_utils import receive_message,send_message,receive_username,send_username,exchange_keys

HOST = "127.0.0.1"
PORT = 12345  # Range 0 - 65538

def main():
    # Creating Socket (tcp protocol)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the Server using Host and Address as in server
        server.connect((HOST, PORT))
        print("Connected to Server Successfully 😉")


    except:
        print(f"Unable to Connect to Server {HOST} {PORT}")

    # Exchange Keys
    e,d,n,n_client,e_client=exchange_keys(server)

    # print(e,d,n,n_client,e_client)


    # Send him your username
    username=input("Enter your username ")
    send_username(server,username,e_client,n_client)

    # Receive client username 
    print("Waiting for your friend 🚶‍♀️ .... ")
    server_username=receive_username(server,d,n)


    print(f"Started Chatting with {server_username} 🚀🚀")

    # Start a new thread to Receive messages
    threading.Thread(target=receive_message,args=(server,server_username,d,n)).start()
    # receive_message(server,server_username,d,n)
    
    # Send Message Using Current Thread
    send_message(server,e_client,n_client)

    
if __name__ == "__main__":
    main()
