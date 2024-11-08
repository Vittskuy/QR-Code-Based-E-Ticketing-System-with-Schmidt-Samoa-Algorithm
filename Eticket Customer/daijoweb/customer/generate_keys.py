# generate_keys.py untuk generasi kunci

import random
from sympy import isprime, lcm, mod_inverse

def generate_prime(bits):
    prime = 1
    while not isprime(prime):
        prime = random.getrandbits(bits)
    return prime

def generate_keys(bits=256):
    p = generate_prime(bits)
    q = generate_prime(bits)
    # kunci private n untuk enkripsi
    n = p**2 * q
    pq = p * q
    l = lcm(p-1, q-1)
    # kunci publik d untuk dekripsi
    d = mod_inverse(n, l)
    print("panjang bit p: ",p.bit_length())
    print("panjang bit q: ",q.bit_length())
    print("panjang bit pq: ",pq.bit_length())
    # print("n kunci privat enkripsi: ",n)
    print("panjang bit kunci privat enkripsi n", n.bit_length())
    print("panjang bit kunci publik dekripsi n", d.bit_length())
    return n, d, pq

if __name__ == "__main__":
    # enkripsi dan dekripsi dalam kasus digital signature
    # private key n, public key d, dan pq
    private_key, public_key, pq = generate_keys(256) 
    print("ENCRYPT_KEY_DB =", private_key)
    print("DECRYPT_KEY_DB =", public_key)
    print("PQ_DB =", pq)
