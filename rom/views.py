from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.serializers import serialize

from .models import Arrival, Hotel, Metro, Route, Score
from .forms import SearchForm

from collections import OrderedDict
from operator import itemgetter


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            #search_result = form.search()

            metro = form.cleaned_data['city']
            arrival = form.cleaned_data['arrival']
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            metro_id = Metro.objects.get(name=metro).id
            arrival_id = Arrival.objects.get(name=arrival).id
            #return render(request, 'rom/results.html', {'form': form, 'search_result': search_result})
            return HttpResponseRedirect(reverse('rom:results', args=(metro_id,arrival_id,)))
    else:
        form = SearchForm()
    return render(request, 'rom/index.html', {'form': form})

def results(request, metro_id, arrival_id):
    metro = get_object_or_404(Metro, pk=metro_id)
    map_center = [metro.centroid.coords[1], metro.centroid.coords[0]]
    routes = Route.objects.filter(operator__metro=metro)
    hotels = Hotel.objects.filter(metro=metro)
    hotel_scores = {}
    hotel_images = {}
    for h in hotels:
        hotel_scores[h.name] = round(h.score.qtr_score(arrival_id))
        hotel_images[h.name] = h.image_set.first()
    sorted_hotels = OrderedDict(sorted(hotel_scores.items(), key=itemgetter(1), reverse=True))

    #sorted_hotels = sorted(hotel_scores.items(), key=lambda x:x[1], reverse=True)
    #sorted_hotels = sorted(hotels, key= lambda t: t.score.qtr_score(arrival_id), reverse=True)
    geojson = serialize('geojson', hotels,
        geometry_field='geom', fields=('name','hotel.score.qtr_trips',))

    routes_geojson = serialize('geojson', routes, geometry_field='geom', fields = ('name', 'color', 'vehicle_type',))
    context = {
        'metro': metro,
        'map_center': map_center,
        'sorted_hotels': sorted_hotels,
        'hotel_images': hotel_images,
        'geojson': geojson,
        'routes': routes_geojson
    }

    return render(request, 'rom/results.html', context)


def detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    return render(request, 'rom/detail.html', {'hotel': hotel})
