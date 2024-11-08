from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from customer.models import Ticket
from customer.utils import decrypt_data, encrypt_data, decrypt_data_db, encrypt_data_db
import cv2
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import numpy as np
from pyzbar.pyzbar import decode
import logging
import time

# Inisialisasi logger untuk cek error di command prompt
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
# halaman login admin
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admindaijo' and password == 'daijoqr':
            # Buat sesi login
            request.session['is_logged_in'] = True
            return JsonResponse({'success': True, 'redirect_url': reverse('scan_qr_code')})  # Redirect ke halaman scan QR code
        else:
            return JsonResponse({'success': False, 'message': 'Login gagal'})  # Tampilkan pesan error
    return render(request, 'adminapp/login.html')

# Dekorator untuk memastikan pengguna sudah login
def login_required_view(view):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_logged_in'):
            return HttpResponseRedirect(reverse('admin_login'))
        return view(request, *args, **kwargs)
    return wrapper

@login_required_view
# halaman untuk scan qr code
def scan_qr_code(request):
    return render(request, 'adminapp/scan_qr_code.html')

@login_required_view
# halaman scan qr code setelah berhasil qr discan
def validate_ticket(request):
    if request.method == 'POST':
        start_time = time.time()  # Mulai mengukur waktu
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
            
            #logger isi tiket setelah displit
            logger.debug(f"Name: {name}, Seating Plan: {seating_plan}, Seat Number: {seat_number}")
            
            # cocokan cipherteks variabel dengan database
            try:
                # mencari data di database
                ticket = Ticket.objects.get(
                    name=encrypted_name,
                    seating_plan=encrypted_seating_plan,
                    seat_number=encrypted_seat_number,
                )
                
                # mengecek apakah tiket sudah pernah check-in
                if ticket.check_in:
                    
                    # memberi jeda scan 3 detik agar terlihat jelas waktu scannya
                    time.sleep(3)
                    logger.warning("Tiket sudah digunakan")
                    return JsonResponse({'message': 'Tiket sudah digunakan!'}, status=404)

                # jika belum pernah check-in, maka sekarang status check-in di database diubah menjadi True
                ticket.check_in = True
                ticket.save()
                
                end_time = time.time()  # Selesai mengukur waktu
                process_time = end_time - start_time # waktu proses validasi tiket
                logger.info(f"Ticket validation process time: {process_time} seconds")
                
                # Logging jika tiket ditemukan
                logger.debug(f"Tiket valid: {ticket}")
                
                
                
                
                # jika tiket ditemukan, kembalikan respons "Tiket Valid!" beserta informasi tiket
                return JsonResponse({'message': f'Tiket Valid! {name} - {seating_plan} - {seat_number}'})
            # jika tiket tidak ditemukan, tiket tidak valid
            except Ticket.DoesNotExist:
                logger.warning("Tiket tidak valid, detail tiket tidak ditemukan di database")
                return JsonResponse({'message': 'Tiket tidak valid! Detail tiket tidak terdapat di Database!'}, status=404)
        # eror lain
        except Exception as e:
            logger.error(f"Tiket Tidak Valid {str(e)}")
            return JsonResponse({'message': 'Tiket tidak valid!'}, status=404)
    return JsonResponse({'message': 'Metode request tidak valid.'}, status=400)

def admin_logout(request):
    logout(request)
    return redirect('admin_login')