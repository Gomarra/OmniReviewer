from django.shortcuts import render

def paginaHome(request):
    return render(request, "omniReviewer/home.html")