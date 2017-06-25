# Create your views here.
# home_page = None
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    # new_list 구현 후 필요없는 코드 삭제
    # # return HttpResponse('<html><title>To-Do Lists</title></html>')
    # if request.method == "POST":
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/only_one_list_in_the_world/')
    return render(request, 'lists/home.html')


def view_list(request):
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'lists/list.html', context)


def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('only_one_list_in_the_world/')
