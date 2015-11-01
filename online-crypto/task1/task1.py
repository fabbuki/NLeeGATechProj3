#!/usr/bin/python
import binascii
import sys
import time
from des import *

def bintohex(s):
    t = ''.join(chr(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8))
    return binascii.hexlify(t).upper()

def hextobin(s):
    return binascii.unhexlify(s)

def string2array(s):
    my_array = []
    for i in range(len(s)):
        my_array.append(int(s[i]))
    return my_array


def test():
    key1 = b"\0\0\0\0\0\0\0\0"
    key2 = b"\0\0\0\0\0\0\0\2"
    message1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    message2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    test_des(key1, message1)
    test_des(key1, message2)
    test_des(key2, message1)
    test_des(key2, message2)

def test_des(key, message):
    k = des(key)
    c = k.des_encrypt(message)
    print bintohex("".join([str(e) for e in c]))

def cbc_encrypt(message, key, iv):
    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      ciphertext: string
    """
    # TODO: Add your code here.
    b = bin(int(binascii.hexlify(message),16))
    b = b[2:]

    b = string2array(b)
    print b
    print type(b)

    #experimental
    message_bytearray = bytearray(message)
    message = message_bytearray #testing testing testing This should convert the message to a bytearray

    print "The message length is"
    print len(message)
    print [x for x in message]

    test()
    #padding
    ultimate_string_length = len(message)
    if len(message)%8 == 0:
        special_string = [1]
        special_string = special_string + [0]*63
        print "special string is"
        print special_string
        message.append(special_string)
    else:
        while(ultimate_string_length%8 != 0):
            ultimate_string_length += 1
        zero_bit_count = (ultimate_string_length - len(message))*8
        special_string=[1]+ [0]*zero_bit_count
        print "special string is"
        print special_string
        message.append(special_string)

    encrypted_string = []

    # while len(message)>0:
    #     subset_string = []
    #     for i in range(0,7,1):
    #         subset_string.append(message[0])
    #         del message[0]
    #         print len(message) #sanity check
    myDes = des(hextobin(key))
    c = myDes.des_encrypt(message)

    return bintohex("".join([str(e) for e in c]))

def cbc_decrypt(message, key, iv):
    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      plaintext: string
    """
    # TODO: Add your code here.

    test()

    k = des(hextobin(key))
    c = k.des_decrypt(message)

    return bintohex("".join([str(e) for e in c]))

def main(argv):
    if len(argv) != 5:
        print 'Wrong number of arguments!\npython task1.py $MODE $INFILE $KEYFILE $IVFILE $OUTFILE'
        sys.exit(1)
    mode = argv[0]
    infile = argv[1]
    keyfile = argv[2]
    ivfile = argv[3]
    outfile = argv[4]
    message = None
    key = None
    iv = None
    try:
        message = open(infile, 'r').read()
        key = open(keyfile, 'r').read()
        iv = open(ivfile, 'r').read()
    except:
        print 'File Not Found'
    start = time.time()
    if mode == "enc":
        output = cbc_encrypt(message, key, iv)
    elif mode == "dec":
        output = cbc_decrypt(message, key, iv)
    else:
        print "Wrong mode!"
        sys.exit(1)
    end = time.time()
    print "Consumed CPU time=%f"% (end - start)
    open(outfile, 'w').write(output)

if __name__=="__main__":
    main(sys.argv[1:])
