from django.shortcuts import render
from .models import Trail, Park


def catalog(request):
    trails = Trail.objects.filter(is_open=True).order_by("distance_km")
    return render(request, "catalog.html", {"trails": trails})


def by_park(request, park_id):
    park = Park.objects.get(id=park_id)
    trails = Trail.objects.filter(park=park, is_open=True).order_by("distance_km")
    return render(request, "catalog.html", {"trails": trails})