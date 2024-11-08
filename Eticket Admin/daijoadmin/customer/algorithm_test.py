# testing algoritma schdmidt samoa

import random
from sympy import isprime, lcm, mod_inverse
import json

# fungsi untuk generate keys
def generate_prime(bits):
    prime = 1
    while not isprime(prime):
        prime = random.getrandbits(bits)
    return prime

def generate_keys(bits=256):
    p = generate_prime(bits)
    q = generate_prime(bits)
    # kunci publik n
    n = p**2 * q
    # pq untuk dekripsi
    pq = p * q
    # kunci privat
    l = lcm(p-1, q-1)
    d = mod_inverse(n, l)
    return n, d, pq


# fungsi enkripsi dan dekripsi schmidt-samoa
def encrypt(public_key, message):
    n = public_key
    m = int.from_bytes(message.encode(), 'big')
    c = pow(m, n, n)
    return c

def decrypt(private_key, pq, ciphertext):
    d = private_key
    m = pow(ciphertext, d, pq)
    message_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
    return message_bytes.decode()

# fungsi untuk memecah pesan menjadi blok blok kecil
def encrypt_long_message(public_key, message, block_size=31):
    blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]
    encrypted_blocks = [encrypt(public_key, block) for block in blocks]
    return json.dumps(encrypted_blocks) # Convert to JSON string

def decrypt_long_message(private_key, pq, ciphertext_json):
    encrypted_blocks = json.loads(ciphertext_json) # Convert from JSON string
    print(f"Encrypted blocks: {encrypted_blocks} (type: {type(encrypted_blocks)})")
    decrypted_blocks = [decrypt(private_key, pq, int(block)) for block in encrypted_blocks]
    return ''.join(decrypted_blocks)

# Pembangkitan kunci
n, d, pq = generate_keys(256)
public_key = n
private_key = d

# Pengujian enkripsi dan dekripsi
message = "vitoadinugroho2207@gmail.com Abcdefghijkaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaedad"
print("Message:", message)
print("Public Key:", public_key)
print("Private Key:", private_key)

# Encrypt a long message
encrypted_message = encrypt_long_message(public_key, message) # ciphertext = encrypt(public_key, message)
print('')
print("Encrypted:", encrypted_message)

# Decrypt the long message
decrypted_message = decrypt_long_message(private_key, pq, encrypted_message) # decrypted_message = decrypt(private_key, pq, encrypted_message)
print("Decrypted:", decrypted_message)

print('')
print(f"Public key (n) length: {len(str(n))} characters")
print(f"Private key (d) length: {len(str(d))} characters")
print(f"pq length: {len(str(pq))} characters")
print(f"chiper (c) length: {len(str(encrypted_message))} characters")

print('')
#apabila hasil dekripsi tidak sama dengan message awal, kirim pesan error
assert message == decrypted_message, "The decrypted message does not match the original message!"
print("Encryption and decryption successful!")

