import json
import qrcode
from django.core.mail import EmailMessage
from django.conf import settings
# utils.py berisi kumpulan fungsi-fungsi yang digunakan: kriptografi + generate qr code + send email

# fungsi enkripsi dan dekripsi schmidt-samoa untuk tandatangan digital
def encrypt(private_key, message):
    n = private_key
    m = int.from_bytes(message.encode(), 'big')
    c = pow(m, n, n)
    return c

def decrypt(public_key, pq, ciphertext):
    d = public_key
    m = pow(ciphertext, d, pq)
    message_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
    return message_bytes.decode()

# fungsi partisi pesan panjang menjadi blok-blok kecil agar dapat dienkripsi 
def encrypt_long_message(private_key, message, block_size=31):
    blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]
    encrypted_blocks = [encrypt(private_key, block) for block in blocks]
    return json.dumps(encrypted_blocks) # Convert to JSON string

def decrypt_long_message(public_key, pq, ciphertext_json):
    encrypted_blocks = json.loads(ciphertext_json) # Convert from JSON string
    decrypted_blocks = [decrypt(public_key, pq, int(block)) for block in encrypted_blocks]
    return ''.join(decrypted_blocks)

# fungsi wrapper untuk enkripsi data dan dekripsi data customer pada qr code
def encrypt_data(data):
    private_key = settings.PRIVATE_KEY
    return encrypt_long_message(private_key, data) #JSON String

def decrypt_data(data):
    public_key = settings.PUBLIC_KEY
    pq = settings.PQ
    return decrypt_long_message(public_key, pq, data)

# fungsi wrapper untuk enkripsi data dan dekripsi data pada database
def encrypt_data_db(data):
    encrypt_key_db = settings.ENCRYPT_KEY_DB
    return encrypt_long_message(encrypt_key_db, data) #JSON String

def decrypt_data_db(data):
    decrypt_key_db = settings.DECRYPT_KEY_DB
    pq = settings.PQ_DB
    return decrypt_long_message(decrypt_key_db, pq, data)

# QR code generation and email sending
def generate_qr_code(ticket):
    qr_data = f"{ticket.name}|{ticket.seating_plan}|{ticket.seat_number}"
    # enkripsi data pada qr
    encrypted_data = encrypt_data(qr_data)
    encrypted_data_str = json.dumps(encrypted_data)
    
    qr = qrcode.QRCode(
        version=10,  # Menggunakan QR Code versi 10
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(encrypted_data_str)
    qr.make(fit=True)
    
    qr_code = qr.make_image(fill='black', back_color='white')
    qr_code_path = f'media/qr_codes/{ticket.email}.png'
    qr_code.save(qr_code_path)
    
    return qr_code_path

def send_email(ticket, qr_code_path):
    email = EmailMessage(
        'QR Code Daijo Ticket',
        f'Terima kasih telah membeli tiket Daijo Ticket!\n\nBerikut adalah detail pembelian Anda:\n\nNama: {ticket.name}\nEmail: {ticket.email}\nTelepon: {ticket.phone}\nSeating Plan: {ticket.seating_plan}\nNomor Kursi: {ticket.seat_number}\n\nQR code tiket Anda terlampir pada email ini.',
        'your-email@example.com',
        [ticket.email],
    )
    email.attach_file(qr_code_path)
    email.send()