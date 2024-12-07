from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class BookingForm(forms.Form):
    num_seats = forms.IntegerField(min_value=1, label='Number of Seats')