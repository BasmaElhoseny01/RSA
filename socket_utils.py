from itertools import zip_longest
from RSA import generate_keys, encrypt, decrypt


def receive_message(client, username, d, n):
    # Listen for messages from the client
    while 1:
        received_list=client.recv(2048).decode('utf-8').split('\n')

        plain_text=decrypt_message(received_list, d, n)
        print(f"{username}:",plain_text)



def send_message(client, e, n):
    # Send messages from the client
    while 1:
        message = input()
        m_list = encrypt_message(message,e,n)
        
        client.sendall(str.encode("\n".join(m_list)))


def send_username(client, username, e, n):
    client.sendall(username.encode())
    return username


def receive_username(client, d, n):
    username = client.recv(2048).decode('utf-8')
    return username


def exchange_keys(client):
    # Generating RSA Keys 😀
    e, d, n = generate_keys(100)


    # Send Your public key<e,d> to the other user
    client.sendall(str.encode("\n".join([str(n), str(e)])))


    # Receive Other's public key <e,n>
    n_client, e_client = [str(i) for i in client.recv(
        2048).decode('utf-8').split('\n')]

    # print("Sent",n)
    # print("Sent",e)

    # print("Received",n_client)
    # print("Received",e_client)


    return e, d, n, int(n_client), int(e_client)


def map_alphabet(c):
    if (c >= 48 and c <= 57):
        return c-48
    elif (c >= 97 and c <= 122):
        return c-87
    else:
        return 36
    

def map_alphabet_inverse(c):
    if (c >= 0 and c <= 9):
        return c+48
    elif (c >= 10 and c <= 35):
        return c+87
    else:
        # space
        return 32



def encrypt_message(message, e, n):
    # Convert to list of ascii
    m = [ord(c) for c in message]

    m_encoded = list(map(map_alphabet, m))

    # Split List into Groups of 5
    list_of_groups = list(zip_longest(*(iter(m_encoded),) * 5))
    i = 0

    encrypted_message=list_of_groups

    for list_item in list_of_groups:
        # Encode
        encoded = plaintext_number(list_item)
        
        # Encrypt
        encrypted_message[i]=str(encrypt(encoded, e, n))
        i = i+1

    return encrypted_message


def decrypt_message(cipher, d, n):
    i=0
    plain_text=""
    for c in cipher:
        # Decrypt
        decrypted=decrypt(int(c), d, n)

        # Decode
        plain_text+= number_plaintext(decrypted)

    return plain_text

def plaintext_number(list_number):
    count = 0
    for i in range(0, 5):
        if list_number[i]==None:
            #  Replace None with space
             count = count+36*pow(37, 4-i)
        else:
            count = count+list_number[i]*pow(37, 4-i)

    return count

def number_plaintext(number):
    plain_text=""
    
    for i in range(0, 5):
        # Map to character then convert int tASCI
        plain_text+=chr(map_alphabet_inverse(number%37))
        number=(number-number%37)//37
    return plain_text[::-1]