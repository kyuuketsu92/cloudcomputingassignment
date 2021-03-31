#this module will handle all the encryption and decryption requests for the auth module and any db read modules
import math
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def get_chiper():
    #get key
    f = open("advertisements","rb")
    key = f.read(32)
    iv = f.read(16)
    f.close()

    return Cipher(algorithms.AES(key), modes.CBC(iv))

def encrypt(data): #string to hexstring
    #we gotta bring the info to a multiplicand of the AES key size of 32
    #since everything is stored as VARCHAR in the database I think a simple '/0' padding for the byte array might be sufficient
    #print(data)


    #get data size
    size = len(data)
    #print(size)
    
    #get the final size we need
    mult = math.ceil(size/32)
    #print(mult)

    
    #convert the string argument into binary
    encoded_string = data.encode()
    #print(encoded_string)

    #in byte array we can add null terminators
    xs = bytearray(encoded_string)
    for i in range((mult*32)-size):
        xs.append(0)

    #print(str(xs))
    #print(len(xs))
    #print(xs.decode('utf_8'))

    #initialise encryptor
    cipher = get_chiper()
    encryptor = cipher.encryptor()

    #encrypt
    ct = encryptor.update(xs) + encryptor.finalize()

    #test if the whole decrypt will work
    #print(str(ct))
    #decryptor = cipher.decryptor()
    #print((decryptor.update(ct)+decryptor.finalize()).decode('utf_8').replace('\0','')+":EOS")
    retval = ''.join('{:02x}'.format(x) for x in ct)
    return retval

def decrypt(data): #hexstring to string

    data = bytearray.fromhex(data)
    #initialise decryptor
    cipher = get_chiper()
    decryptor = cipher.decryptor()

    #encrypt
    ct = decryptor.update(data) + decryptor.finalize()
    ct = ct.decode('utf_8').replace('\0','')

    return ct

def gen_auth_key():
    key = os.urandom(128)
    return ''.join('{:02x}'.format(x) for x in key)