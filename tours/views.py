import random

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

from tours.data import departures, description, subtitle, title, tours


def main_view(request):
    random_tours = {}
    while len(random_tours) < 6:
        random_id = random.choice(list(tours.keys()))
        if random_id not in random_tours:
            random_tours[random_id] = tours[random_id]
    return render(request, 'index.html',
                  context={'title': title, 'departures': departures, 'subtitle': subtitle, 'description': description,
                           'random_tours': random_tours})


def departure_view(request, departure: str):
    dept = departures[departure][0].lower() + departures[departure][1:]
    dept_tours = {}
    for tour_id, tour in tours.items():
        if departure == tour['departure']:
            dept_tours[tour_id] = tour
    min_price = min([tour['price'] for tour in dept_tours.values()])
    max_price = max([tour['price'] for tour in dept_tours.values()])
    min_nights = min([tour['nights'] for tour in dept_tours.values()])
    max_nights = max([tour['nights'] for tour in dept_tours.values()])
    return render(request, 'departure.html',
                  context={'title': title, 'departures': departures, 'departure': dept, 'tours': dept_tours,
                           'min_nights': min_nights, 'max_nights': max_nights, 'min_price': min_price,
                           'max_price': max_price})


def tour_view(request, id: int):
    tour = tours[id]
    stars_range = range(int(tour['stars']))
    departure_name = departures[tour['departure']][0].lower() + departures[tour['departure']][1:]
    return render(request, 'tour.html',
                  context={'title': title, 'departures': departures, 'tour': tour, 'stars_range': stars_range,
                           'departure_name': departure_name})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
