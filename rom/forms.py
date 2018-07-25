from django import forms
from decouple import config
import time, hashlib
import json
import requests

from .models import Metro, Arrival, Hotel


class SearchForm(forms.Form):
    city = forms.ModelChoiceField(queryset=Metro.objects.all())
    arrival = forms.ModelChoiceField(queryset=Arrival.objects.all())
    check_in = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'date'}))
    check_out = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'date'}))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].empty_label = 'city'
        self.fields['arrival'].empty_label = 'arrival location'

    def search(self):
        metro = Metro.objects.get(name=self.cleaned_data['city'])
        check_in = self.cleaned_data['check_in']
        check_out = self.cleaned_data['check_out']

        hotel_list = []
        metro_hotels = Hotel.objects.filter(metro=metro)
        for hotel in metro_hotels:
            hotel_list.append(hotel.hotel_code)

        URL = "https://api.test.hotelbeds.com/hotel-api/1.0/hotels"
        sig_str = "%s%s%d" % (config('API_KEY'),config('SECRET'),int(time.time()))
        signature = hashlib.sha256(sig_str.encode('utf-8')).hexdigest()

        headers = {
            "X-Signature": signature,
            "Api-Key": config('API_KEY'),
            "Accept": "application/json"
        }

        params = {
        	"stay": {
        		"checkIn": check_in,
        		"checkOut": check_out
        	},
        	"occupancies": [{
        		"rooms": 1,
        		"adults": 2,
        		"children": 0
        	}],
        	"hotels": {
        		"hotel": hotel_list
        	},
        	"accommodations": ["HOTEL"],
        	"dailyRate": True
        }

        r = requests.post(url=URL, headers=headers, params=params)
        available_hotels = r.json()
        return available_hotels
