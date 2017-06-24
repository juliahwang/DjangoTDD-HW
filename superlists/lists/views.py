# Create your views here.
# home_page = None
from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    # return HttpResponse('<html><title>To-Do Lists</title></html>')
    return render(request, 'lists/home.html')