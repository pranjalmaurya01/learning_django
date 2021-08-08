from django.db import models
from django.http.response import HttpResponse

# Create your models here.


def home(request):
    print(request)
    return(HttpResponse('YO home ?'))
