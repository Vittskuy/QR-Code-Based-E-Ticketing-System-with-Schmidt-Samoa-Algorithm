from django import forms

# form data customer yang harus diisi 

class TicketForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, label='Phone')
    SEATING_PLANS = [
        ('Festival', 'Festival'),
        ('CAT 1', 'CAT 1'),
        ('CAT 2', 'CAT 2'),
        ('CAT 3', 'CAT 3'),
        ('CAT 4', 'CAT 4'),
    ]
    seating_plan = forms.ChoiceField(choices=SEATING_PLANS, label='Seating Plan')
    SEAT_NUMBERS = [(i, str(i)) for i in range(1, 11)]
    seat_number = forms.ChoiceField(choices=SEAT_NUMBERS, label='Seat Number')