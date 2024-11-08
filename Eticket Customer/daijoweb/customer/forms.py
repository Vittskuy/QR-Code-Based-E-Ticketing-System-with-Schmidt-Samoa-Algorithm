from django import forms

class TicketForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nama')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, label='Nomor Telepon')
    
    SEATING_PLANS = [
        ('', 'Pilih'),  # Nilai default kosong
        ('Festival', 'Festival'),
        ('CAT 1', 'CAT 1'),
        ('CAT 2', 'CAT 2'),
        ('CAT 3', 'CAT 3'),
        ('CAT 4', 'CAT 4'),
    ]
    seating_plan = forms.ChoiceField(choices=SEATING_PLANS, label='Seating Plan', required=True)
    
    SEAT_NUMBERS = [('', 'Pilih')] + [(i, str(i)) for i in range(1, 11)]  # Nilai default kosong
    seat_number = forms.ChoiceField(choices=SEAT_NUMBERS, label='Seat Number', required=True)

    def clean_seating_plan(self):
        seating_plan = self.cleaned_data.get('seating_plan')
        if seating_plan == '':
            raise forms.ValidationError('Please select a valid seating plan.')
        return seating_plan

    def clean_seat_number(self):
        seat_number = self.cleaned_data.get('seat_number')
        if seat_number == '':
            raise forms.ValidationError('Please select a valid seat number.')
        return seat_number
