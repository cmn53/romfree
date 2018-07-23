from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.serializers import serialize
from django.db.models import F, Sum
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Arrival, Hotel, HotelArrival, Metro, Route, Score, Destination
from .forms import SearchForm
import json


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
    arrival = get_object_or_404(Arrival, pk=arrival_id)
    map_center = [metro.centroid.coords[1], metro.centroid.coords[0]]

    routes = Route.objects.filter(operator__metro=metro).exclude(vehicle_type="ferry")
    destinations = Destination.objects.filter(metro=metro)
    hotel_arrival_set = HotelArrival.objects.filter(hotel__metro=metro, arrival=arrival)

    paginator = Paginator(hotel_arrival_set, 20)
    page = request.GET.get('page')
    paginated_hotels = paginator.get_page(page)

    hotel_list = []
    i = (int(page)-1) * 20
    for h in hotel_arrival_set[i:i+20]:
        hotel_list.append(
            {
                "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [h.hotel.geom.coords[0], h.hotel.geom.coords[1]]
                    },
                    "properties": {
                        "order": len(hotel_list),
                        "name": h.hotel.name,
                        "score": h.total_qtr_score
                    }
            }
        )
    hotel_geojson = json.dumps(hotel_list)

    route_geojson = serialize(
        'geojson',
        routes,
        geometry_field='geom',
        fields=('name', 'vehicle_type',)
    )

    destination_geojson = serialize(
        'geojson',
        destinations,
        geometry_field='geom',
        fields=('name',)
    )



    context = {
        'metro': metro,
        'map_center': map_center,
        'hotels': paginated_hotels,
        'hotel_geojson': hotel_geojson,
        'route_geojson': route_geojson,
        'destination_geojson': destination_geojson
    }

    return render(request, 'rom/results.html', context)


def detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    return render(request, 'rom/detail.html', {'hotel': hotel})
