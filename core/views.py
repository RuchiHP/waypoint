from django.shortcuts import render

def home(request):
    return render(request, "home.html", {"greeting": "Welcome to Waypoint"})

def report(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        return render(request, "thank_you.html", {"name": name})
    return render(request, "report.html")

def search(request):
    query = request.GET.get("q", "")
    return render(request, "search.html", {"query": query})

def catalog(request):
    trails = [
        {"name": "Bruce Trail", "distance": 12.456, "elevation": 300, "difficulty": "moderate", "is_open": True},
        {"name": "Killarney Loop", "distance": 8.2, "elevation": 150, "difficulty": "easy", "is_open": True},
        {"name": "Algonquin Ridge", "distance": 22.789, "elevation": 900, "difficulty": "expert", "is_open": True},
        {"name": "Frozen Falls Trail", "distance": 5.0, "elevation": 60, "difficulty": "easy", "is_open": False},
        {"name": "Devil's Glen", "distance": 15.3, "elevation": 500, "difficulty": "moderate", "is_open": True},
        {"name": "Summit Peak Route", "distance": 30.1, "elevation": 1200, "difficulty": "expert", "is_open": True},
    ]
    return render(request, "catalog.html", {"trails": trails})