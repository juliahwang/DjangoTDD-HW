import re

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from .models import Item
from .views import home_page


# Create your tests here.
# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)


class HomePageTest(TestCase):
    # csrf_token 에 의해 생성된 input요소값이 달라지므로 정규식으로 삭제해준다.
    pattern_input_csrf = re.compile(r'<input[^>]*csrfmiddlewaretoken[^>]*>')

    def test_root_url_resolves_to_home_page_view(self):
        # resolve('/') : 장고의 내부함수로 url을 해석해서 일치하는 뷰함수를 찾는다.
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)
        # 새 아이템이 데이터베이스에 저장되었는지 확인
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        # 아이템 텍스트가 같은지 확인
        self.assertEqual(new_item.text, '신규 작업 아이템')

    # 아이템저장이 원활한지 윗 테스트를 분할해 새로운 테스트 메서드로 리펙터링
    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        # 응답이 html 에 의해 렌더링되지 않고 redirect되므로 이를 확인하는 코드로 수정.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    # 템플릿이 여러 아이템을 출력할 수 있는지 확인하는 테스트
    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class ItemModelTest(TestCase):
    pattern_input_csrf = re.compile(r'<input[^>]*csrfmiddlewaretoken[^>]*>')

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

