# Create your views here.
# home_page = None
from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>To Do Lists</title></html>')