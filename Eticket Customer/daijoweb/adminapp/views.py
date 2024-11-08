''' from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from customer.models import Ticket
from customer.utils import decrypt_data, encrypt_data, decrypt_data_db, encrypt_data_db
import cv2
from django.http import JsonResponse
import json
import numpy as np
from pyzbar.pyzbar import decode
import logging

# Inisialisasi logger untuk cek error di command prompt
logger = logging.getLogger(__name__)

# halaman login admin
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admindaijo' and password == 'daijoqr':
            return JsonResponse({'success': True, 'redirect_url': 'scan'}) # pindah ke halaman adminapp/scan
        else:
            return JsonResponse({'success': False, 'message': 'Login gagal'}) # pesan error, tetap di halaman yang sama
    return render(request, 'adminapp/login.html')

# halaman untuk scan qr code
def scan_qr_code(request):
    return render(request, 'adminapp/scan_qr_code.html')

# halaman scan qr code setelah berhasil qr discan
def validate_ticket(request):
    if request.method == 'POST':
        qr_code = request.POST['qr_code']
        
        # Debugging log: received QR code
        logging.debug(f"Received QR code: {qr_code} (type: {type(qr_code)})")
        
        try:
            # Convert JSON string dalam qr menjadi list of integers
            encrypted_blocks = json.loads(qr_code)
            
            # dekripsi data dari qr yang telah bertipe list of integer
            decrypted_qr_code = decrypt_data(encrypted_blocks)
            # Logging hasil dekripsi
            logging.debug(f"Decrypted QR code: {decrypted_qr_code} (type: {type(decrypted_qr_code)})")
            
            # validasi apakah qr asli dan memiliki 2 pemisah "John|CAT1|2"
            if decrypted_qr_code.count('|') != 2:
                return JsonResponse({'message': 'Tiket Anda Tidak Valid!'}, status=404)
            
            # jika valid, string dipisah menjadi  variabel nama, seating_plan, dan seat_number "John", "CAT1, "2"
            name, seating_plan, seat_number = decrypted_qr_code.split('|')
            
            # enkripsi variabel untuk dicocokan ke database
            encrypted_name = encrypt_data_db(name)
            encrypted_seating_plan = encrypt_data_db(seating_plan)
            encrypted_seat_number = encrypt_data_db(seat_number)
            
            # cocokan cipherteks variabel dengan database
            try:
                # mencari data di database
                ticket = Ticket.objects.get(
                    name=encrypted_name,
                    seating_plan=encrypted_seating_plan,
                    seat_number=encrypted_seat_number,
                )
                # jika tiket ditemukan, kembalikan respons "Tiket Valid!" beserta informasi tiket
                return JsonResponse({'message': f'Tiket Valid! {name} - {seating_plan} - {seat_number}'})
            # jika tiket tidak ditemukan, tiket tidak valid
            except Ticket.DoesNotExist:
                return JsonResponse({'message': 'Detail tiket Anda tidak terdapat di Database!'}, status=404)
        # eror lain
        except Exception as e:
            logger.error(f"Error saat dekripsi atau validasi tiket: {str(e)}")
            return JsonResponse({'message': 'Tiket tidak valid, tidak dapat didekripsi!'}, status=404)
    return JsonResponse({'message': 'Metode request tidak valid.'}, status=400)
    
'''