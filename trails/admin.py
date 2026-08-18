from django.contrib import admin
from .models import Trail, Park


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
    search_fields = ("name",)


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ("name", "distance_km", "elevation_gain", "difficulty", "is_open", "park", "added")
    search_fields = ("name",)
    list_filter = ("park",)