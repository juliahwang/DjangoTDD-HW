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

        # 응답이 html 에 의해 렌더링되지 않고 redirect되므로 이를 확인하는 코드로 수정.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

        # self.assertIn('A new list item', response.content.decode())
        # expected_html = render_to_string(
        #     'lists/home.html',
        #     {
        #         'new_item_text': 'A new list item',
        #     }
        # )
        # self.assertEqual(
        #     re.sub(self.pattern_input_csrf, '', response.content.decode()),
        #     re.sub(self.pattern_input_csrf, '', expected_html)
        # )


    # def test_home_page_returns_correct_html(self):
    #     # HttpRequest 객체를 생성해 어떤 요청을 브라우저에 보내는지 확인
    #     request = HttpRequest()
    #     request.method = 'POST'
    #     request.POST['item_text'] = '신규 작업 아이템'
    #     # home_page 뷰에 전달해서 HttpResponse 객체로 응답을 받는다.
    #     response = home_page(request)
    #     self.assertIn('신규 작업 아이템', response.content.decode())
    #     expected_html = render_to_string(
    #         'lists/home.html',
    #         {
    #             'new_item_text': '신규 작업 아이템',
    #         }
    #     )
    #     # decode()를 사용해 expected_html의 byte 데이터를 파이썬 유니코드 문자열로 변환.
    #     self.assertEqual(
    #         re.sub(self.pattern_input_csrf, '', response.content.decode()),
    #         re.sub(self.pattern_input_csrf, '', expected_html)
    #     )

        ######### 상수/문자열은 테스트 범위가 아니므로 위처럼 변경 ############
        # # byte형 데이터인 <html></html>로 구성되어 있는지 확인
        # self.assertTrue(response.content.startswith(b'<html>'))
        # # title에 특정 단어가 있는지 확인
        # self.assertIn(b'<title>To-Do Lists</title>', response.content)
        # self.assertTrue(response.content.endswith(b'</html>'))

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


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

