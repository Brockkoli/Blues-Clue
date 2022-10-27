from Cryptodome.Cipher import AES
from hashlib import md5
import pyfiglet

def msg():
    title = pyfiglet.figlet_format("AES Decryptor for Blue's Clues")
    print(title)
    print("\nUsage: ")
    print("[*]  Input encrypted filename.")
    print("[*]  Input password.\n")

def getKeyAndIv(password, salt, keyLength, ivLength): # get key and IV from the pw and salt.
    d = d_i = b''
    while len(d) < keyLength + ivLength:
        d_i = md5(d_i + str.encode(password) + salt).digest() # get md5 hash value
        d += d_i
    return d[:keyLength], d[keyLength:keyLength+ivLength]

def decrypt(inputFile, outputFile, password, keyLength=32):
    bs = AES.block_size # 16 bytes
    salt = inputFile.read(bs)
    key, iv = getKeyAndIv(password, salt, keyLength, bs)
    # MODE_CBC or Ciphertext Block Chaining
    # each block of plaintext XOR with previous ciphertext block before encryption
    cipher = AES.new(key, AES.MODE_CBC, iv)
    nextChunk = ''
    complete = False
    while not complete:
        chunk, nextChunk = nextChunk, cipher.decrypt(inputFile.read(1024 * bs))
        if len(nextChunk) == 0:
            paddingLength = chunk[-1]
            chunk = chunk[:-paddingLength]
            complete = True 
        outputFile.write(bytes(x for x in chunk)) 

if __name__ == '__main__':
    msg()
    plaintextFile = input("Input the name of the encrypted file with extension: ") # target.xlsx
    password = input("Input your password: ") # 31337
    with open(plaintextFile, 'rb') as inputFile, open('decryptedFile.xlsx', 'wb') as outputFile:
        decrypt(inputFile, outputFile, password)
        print("\n[*] File decrypted...")