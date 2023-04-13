from RSA import *
from socket_utils import encrypt_message,decrypt_message

def main():
    message="hello i am basma elhoseny 01"
    key_sizes=[8,10,16,20,32,40,50,60,64,70]


    
    for key_size in key_sizes:
        print("Key size ",key_size)

        start=time.time()
        e, d, n = generate_keys(key_size)
        end=time.time()
        print("e",e,"d",d,"n",n)
        generate_key_time=end-start

        start=time.time()
        cipher=encrypt_message(message,e,n)
        end=time.time()
        encrypt_time=end-start

        start=time.time()
        plain_text=decrypt_message(cipher, d, n)
        end=time.time()
        decrypt_time=end-start


        start=time.time()
        d_broken=breakRSA(e, n)
        end=time.time()
        attack_time=end-start

        # Use this e to decrypt Message 🦹‍♀️
        decrypt_attacked=decrypt_message(cipher, d_broken, n)

        print("key 🔑 size:",key_size)
        print("key generated (sec):",generate_key_time)
        print("Encryption 🔐 (sec):",encrypt_time)
        print("Decryption 🔓 (sec):",decrypt_time)
        print("Attack 😈😈 (sec):",attack_time)
        print("Decrypted text(by receiver not attacked):",plain_text)
        if(decrypt_attacked==message):
            print("RSA Key Broken Successfully 🙄")
            print("Believe it or not the private key : ",d_broken," 🎃😈")
            print("The Decrypted message is:",)
        else :
            print("Failed to break RSA")
        print("************************************************")



if __name__ == "__main__":
    main()