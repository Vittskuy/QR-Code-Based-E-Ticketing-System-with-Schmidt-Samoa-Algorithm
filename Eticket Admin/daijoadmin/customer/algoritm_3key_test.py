from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

# Function to derive a shared key from two parts of a shared secret
def derive_shared_key(part1, part2):
    combined = part1 + part2
    return hashlib.sha256(combined.encode()).digest()

# Function to encrypt data deterministically with derived key
def encrypt_deterministic(shared_key, data):
    cipher = AES.new(shared_key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return encrypted_data

# Function to decrypt data
def decrypt_deterministic(shared_key, encrypted_data):
    cipher = AES.new(shared_key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode()

# Shared secret parts known to the database owner and employees
shared_secret_part1 = "part1_of_secret"
shared_secret_part2 = "part2_of_secret"

# Derive the shared key
shared_key = derive_shared_key(shared_secret_part1, shared_secret_part2)

# Encrypt data to be stored in the database
name = "John Doe"
address = "123 Main St"

encrypted_name = encrypt_deterministic(shared_key, name)
encrypted_address = encrypt_deterministic(shared_key, address)

# Store encrypted_name and encrypted_address in the database
database = [(encrypted_name, encrypted_address)]

# Encrypt data to be checked against the database using the same shared key
query_name = "John Doe"
query_address = "123 Main St"

encrypted_query_name = encrypt_deterministic(shared_key, query_name)
encrypted_query_address = encrypt_deterministic(shared_key, query_address)

# Check if the encrypted query data exists in the database
match_found = any(
    encrypted_query_name == row[0] and encrypted_query_address == row[1]
    for row in database
)

print("Match found:", match_found)

# Decrypting to verify correctness
print("Decrypted name:", decrypt_deterministic(shared_key, encrypted_name))
print("Decrypted address:", decrypt_deterministic(shared_key, encrypted_address))