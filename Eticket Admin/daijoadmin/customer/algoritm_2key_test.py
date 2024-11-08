from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib

# Function to derive a shared key from a shared secret
def derive_key(shared_secret):
    return hashlib.sha256(shared_secret.encode()).digest()

# Function to encrypt a message using AES with a derived key
def encrypt_message(shared_secret, message):
    key = derive_key(shared_secret)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes

# Function to decrypt a message using AES with a derived key
def decrypt_message(shared_secret, ciphertext):
    key = derive_key(shared_secret)
    iv = ciphertext[:AES.block_size]
    ct = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

# Shared secret (could be derived from some shared information)
shared_secret_1 = "shared_secret_1"
shared_secret_2 = "shared_secret_2"

# The message to be encrypted
message = "Hello, shared secret encryption!"

# Encrypt the message with both shared secrets
ciphertext_1 = encrypt_message(shared_secret_1, message)
ciphertext_2 = encrypt_message(shared_secret_2, message)

print("Ciphertext with shared secret 1:", ciphertext_1)
print("Ciphertext with shared secret 2:", ciphertext_2)
print("Are the ciphertexts the same?", ciphertext_1 == ciphertext_2)

# Decrypt the message with both shared secrets
decrypted_message_1 = decrypt_message(shared_secret_1, ciphertext_1)
decrypted_message_2 = decrypt_message(shared_secret_2, ciphertext_2)

print("Decrypted Message with shared secret 1:", decrypted_message_1)
print("Decrypted Message with shared secret 2:", decrypted_message_2)