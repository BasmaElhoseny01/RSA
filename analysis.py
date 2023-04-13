from RSA import *
from socket_utils import encrypt_message,decrypt_message

def main():
    message="hello i am basma elhoseny 2001"
    # key_sizes=[8,10,16,20,32,40,50,60,64,70]
    key_sizes=range(28, 51, 1)
    key_generation_time=[]
    encryption_time=[]
    decryption_time=[]
    attacking_time=[]

     
    for key_size in key_sizes:
        print("Key size ",key_size)

        start=time.time()
        e, d, n = generate_keys(key_size)
        end=time.time()
        print("e",e,"d",d,"n",n)
        generate_key_time=end-start
        key_generation_time.append(end-start)

        start=time.time()
        cipher=encrypt_message(message,e,n)
        end=time.time()
        encrypt_time=end-start
        encryption_time.append(end-start)

        start=time.time()
        plain_text=decrypt_message(cipher, d, n)
        end=time.time()
        decrypt_time=end-start
        decryption_time.append(end-start)


        start=time.time()
        d_broken=breakRSA(e, n)
        end=time.time()
        attack_time=end-start
        attacking_time.append(end-start)

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
            print("The Decrypted message is:",decrypt_attacked)
        else :
            print("Failed to break RSA")
        print("************************************************")
    
    #Plotting Results
    plt.plot(key_sizes, key_generation_time)
    plt.title("key_generation_time")
    plt.xlabel("# bits")
    plt.ylabel("time (sec)")
    plt.show()

    plt.plot(key_sizes, encryption_time)
    plt.title("encryption_time")
    plt.xlabel("# bits")
    plt.ylabel("time (sec)")
    plt.show()

    plt.plot(key_sizes, decryption_time)
    plt.title("decryption_time")
    plt.xlabel("# bits")
    plt.ylabel("time (sec)")
    plt.show()

    plt.plot(key_sizes, attacking_time)
    plt.title("attacking_time")
    plt.xlabel("# bits")
    plt.ylabel("time (sec)")
    plt.show()




    # All together
    # Plotting both the curves simultaneously
    plt.plot(key_sizes, key_generation_time,color='g',label='key_generation_time')
    plt.plot(key_sizes, encryption_time,color='b',label='encryption_time')
    plt.plot(key_sizes, decryption_time,color='y',label='decryption_time',linestyle='dashed')
    plt.plot(key_sizes, attacking_time,color='r',label='attacking_time')

    
    # Naming the x-axis, y-axis and the whole graph
    plt.xlabel("# bits")
    plt.ylabel("time (sec)")
    plt.title("RSA Timings Analysis")
    
    # Adding legend, which helps us recognize the curve according to it's color
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()