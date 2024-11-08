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
    n = p**2 * q
    pq = p * q
    l = lcm(p-1, q-1)
    d = mod_inverse(n, l)
    return n, d, pq

if __name__ == "__main__":
    public_key, private_key, pq = generate_keys(256)
    print("PUBLIC_KEY_DB =", public_key)
    print("PRIVATE_KEY_DB =", private_key)
    print("PQ_DB =", pq)
