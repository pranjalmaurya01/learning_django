from django.http.response import HttpResponse
from django.shortcuts import render


def home(request):
    print(request)
    return render(request, 'base.html')
