# Create your views here.
# home_page = None
from django.shortcuts import render


def home_page(request):
    # return HttpResponse('<html><title>To-Do Lists</title></html>')
    context = {
        'new_item_text': request.POST.get('item_text'),
    }
    return render(request, 'lists/home.html', context)
