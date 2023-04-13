from RSA import *
from socket_utils import encrypt_message,decrypt_message

def main():

    print("Welcome to the RSA attack program")

    e=int(input("Enter e to be broken: "))
    n=int(input("Enter n to be broken: "))
    # e=65537 
    # n=2924673163 
    # d=2613129505

    d_broken=breakRSA(e, n)

    print("RSA Key Broken Successfully 🙄")
    print("Believe it or not the private key : ",d_broken," 🎃😈")

    while(True):
        c=input("Enter cipher buckets to be broken separated by -")
        index = c.find('-')
        if index == -1:
            c=[c]
        else:
            c=list(c.split("-"))
        m_broken=decrypt_message(c, d_broken, n)
        print("plain text is",m_broken)


      
if __name__ == "__main__":
    main()