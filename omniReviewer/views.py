from django.http import HttpResponse
from django.shortcuts import render

def paginaHome(request):
    return HttpResponse('Home')