from django.shortcuts import render, redirect
from .models import Ticket
from .forms import TicketForm
from django.core.mail import send_mail
from .utils import generate_qr_code, send_email, encrypt_data, decrypt_data, encrypt_data_db, decrypt_data_db
import json

# halaman home
def home(request):
    if request.method == 'POST':
        event = request.POST.get('event')
        return redirect('details')
    return render(request, 'customer/home.html')

# halaman isi detail tiket
def details(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            request.session['ticket_data'] = form.cleaned_data
            return redirect('confirmation')
    else:
        form = TicketForm()
    return render(request, 'customer/details.html', {'form': form})

# halaman konfimasi
def confirmation(request):
    ticket_data = request.session.get('ticket_data')
    if request.method == 'POST':
        if 'edit' in request.POST:
            return redirect('details')
        # ketika pencet buy, lakukan enkripsi data lalu save ticket, buat qr code 
        elif 'buy' in request.POST:
            # tiket asli untuk qr code
            ticketqr = Ticket(
                name=ticket_data['name'],
                email=ticket_data['email'],
                phone=ticket_data['phone'],
                seating_plan=ticket_data['seating_plan'],
                seat_number=ticket_data['seat_number'],
            )
            # tiket yang dienkripsi untuk database
            ticketdb = Ticket(
                # enkripsi tiket pada database
                name=encrypt_data_db(ticket_data['name']),
                email=encrypt_data_db(ticket_data['email']),
                phone=encrypt_data_db(ticket_data['phone']),
                seating_plan=encrypt_data_db(ticket_data['seating_plan']),
                seat_number=encrypt_data_db(str(ticket_data['seat_number'])),
            )
            # menyimpan tiket yang dienkripsi untuk database
            ticketdb.save()
            # menggenerasi qr code menggunakan tiket asli yang belum dienkripsi
            qr_code = generate_qr_code(ticketqr)
            send_email(ticketqr, qr_code)
            return redirect('thankyou')
    return render(request, 'customer/confirmation.html', {'ticket_data': ticket_data})

# halaman terimakasih
def thankyou(request):
    return render(request, 'customer/thankyou.html')

# utility lain
def ticket_detail_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.name = decrypt_data(ticket.name)
    ticket.email = decrypt_data(ticket.email)
    ticket.phone = decrypt_data(ticket.phone)
    ticket.seating_plan = decrypt_data(ticket.seating_plan)
    ticket.seat_number = decrypt_data(ticket.seat_number)
    return render(request, 'customer/ticket_detail.html', {'ticket': ticket})