# Create your views here.
# home_page = None
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    # return HttpResponse('<html><title>To-Do Lists</title></html>')
    if request.method == "POST":
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')
    else:
        new_item_text = ''
    context = {
        'new_item_text': new_item_text,
    }
    return render(request, 'lists/home.html', context)
