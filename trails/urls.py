from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalog, name="trails-catalog"),
    path("park/<int:park_id>/", views.by_park, name="trails-by-park"),
]