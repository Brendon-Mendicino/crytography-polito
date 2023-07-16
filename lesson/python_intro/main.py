from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

if __name__ == "__main__":
    IV = get_random_bytes(AES.block_size)

    key = get_random_bytes(AES.key_size[2])

    plaintext = b'These are the data to encrypt !!'
    print(len(plaintext))
    
    # Generate an object to mange the encryption
    
    cipher_enc = AES.new(key, AES.MODE_CBC, IV)
    ciphertext = cipher_enc.encrypt(plaintext)
    print(ciphertext)
    
    cipher_dec = AES.new(key, AES.MODE_CBC, IV)
    decrypted = cipher_dec.decrypt(ciphertext)
    print(decrypted)

    
    plaintext = b'Unaligned string...'
    print(len(plaintext))
    cipher_enc = AES.new(key, AES.MODE_CBC, IV)
    padded_data = pad(plaintext, AES.block_size)
    print(padded_data)
    
    ciphertext = cipher_enc.encrypt(padded_data)
    print(ciphertext)

    cipher_dec = AES.new(key, AES.MODE_CBC, IV)
    decrypted = cipher_dec.decrypt(ciphertext)
    print(decrypted)
    
    unpadded_data = unpad(decrypted, AES.block_size)
    print(unpadded_data)