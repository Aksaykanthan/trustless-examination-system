import random
import math

# A set will be the collection of prime numbers,
# where we can select random primes p and q
prime = set()

public_key = None
private_key = None
n = None

# Function to fill the set of prime numbers
def primefiller():
    seive = [True] * 250
    seive[0] = False
    seive[1] = False
    for i in range(2, 250):
        for j in range(i * 2, 250, i):
            seive[j] = False

    # Filling the prime numbers
    for i in range(len(seive)):
        if seive[i]:
            prime.add(i)

def pickrandomprime():
    global prime
    k = random.randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)

    ret = next(it)
    prime.remove(ret)
    return ret

def setkeys():
    global public_key, private_key, n
    prime1 = pickrandomprime()  # First prime number
    prime2 = pickrandomprime()  # Second prime number

    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)

    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1

    public_key = e  # Public key remains the same

    # Find private key 'd'
    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1

    private_key = d  # Private key remains the same

# To encrypt the given number (using the private key)
def encrypt(message):
    global private_key, n
    d = private_key
    encrypted_text = 1
    while d > 0:
        encrypted_text *= message
        encrypted_text %= n
        d -= 1
    return encrypted_text

# To decrypt the given number (using the public key)
def decrypt(encrypted_text):
    global public_key, n
    e = public_key
    decrypted = 1
    while e > 0:
        decrypted *= encrypted_text
        decrypted %= n
        e -= 1
    return decrypted

# Convert each character to its ASCII value and encrypt
def encoder(message):
    encoded = []
    # Calling the encrypting function in encoding function
    for letter in message:
        encoded.append(encrypt(ord(letter)))  # Encrypt using private key
    return encoded

# Decrypting function
def decoder(encoded):
    s = ''
    # Calling the decrypting function decoding function
    for num in encoded:
        s += chr(decrypt(num))  # Decrypt using public key
    return s

def start_encrypt(message):
    primefiller()          
    setkeys()             
    coded = encoder(message) 
    return coded, private_key, public_key , n

def encrypt_with_key(message, private_key):
    global n
    encrypted_message = []
    for letter in message:
        # Encrypt the ASCII value of the letter using the provided private key
        encrypted_value = 1
        ascii_value = ord(letter)
        d = private_key
        while d > 0:
            encrypted_value *= ascii_value
            encrypted_value %= n
            d -= 1
        encrypted_message.append(encrypted_value)
    return encrypted_message

def decrypt_with_key(encrypted_text, public_key,n):
    l = []
    for num in encrypted_text:
        e = public_key
        decrypted = 1
        while e > 0:
            decrypted *= num
            decrypted %= n
            e -= 1
        l.append(decrypted)
    return ''.join(chr(num) for num in l)

if __name__ == '__main__':
    message = "Find the number of zeroes at the end of 48!."

    coded,private_key1,public_key1,n = start_encrypt(message) 
    
    print("Initial message:")
    print(message)
    print("\n\nThe encoded message (encrypted by private key):\n")
    print(coded)
    print(public_key1)

    print("\n\nDecrypted message using decrypt_with_key:\n")
    print(decrypt_with_key(coded,public_key1,n))

    message2 = "Hello"
    print("\n\nEncrypting the message 'Hello' using the private key:")
    encrypted_message = encrypt_with_key(message2,private_key1)
    print(encrypted_message)
    print("\n\nDecrypting the message using the public key:")
    print(decrypt_with_key(encrypted_message,public_key1,n))

    print("\n\n\n")
    code = [1720, 1872, 541, 5031, 2742, 7540, 4702, 7540, 541, 5437, 2492, 1872, 1872, 541, 1872, 2492, 1720, 7540, 7540, 4577, 5031, 5437, 4577, 4702, 1720, 2492, 4702, 2492, 2492, 1720, 1872, 541]
    key = 5
    print("Decrypting the message using the public key:")
    print(decrypt_with_key(code,key,n))
