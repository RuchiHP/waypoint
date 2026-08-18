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