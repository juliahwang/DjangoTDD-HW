import re

from django.core.urlresolvers import resolve
from django.http import HttpRequest
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

    # 아이템저장이 원활한지 윗 테스트를 분할해 새로운 테스트 메서드로 리펙터링
    # test_home_page_only_saves_items_when_necessary(self) 삭제

    # test_home_page_can_save_a_POST_request(self),
    # test_home_page_redirects_after_POST(self) 이동해 새 클래스로 정의

    # test_home_page_displays_list_items(self) 함수는 겹치므로 삭제


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


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/only_one_list_in_the_world/')
        self.assertTemplateUsed(response, 'lists/list.html')

    # 템플릿이 여러 아이템을 출력할 수 있는지 확인하는 테스트
    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        # 장고의 TestCase 속성을 사용(self.client)
        # 여기에 테스트할 URL을 .get한다.
        response = self.client.get('/lists/only_one_list_in_the_world/')

        # 응답내용 처리를 자동으로 해주는 장고의 assertContains 메서드 사용
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={
                'item_text': '신규 작업 아이템',
            }
        )
        # 새 아이템이 데이터베이스에 저장되었는지 확인
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        # 아이템 텍스트가 같은지 확인
        self.assertEqual(new_item.text, '신규 작업 아이템')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={
                'item_text': '신규 작업 아이템',
            }
        )
        # 응답이 html 에 의해 렌더링되지 않고 redirect되므로 이를 확인하는 코드로 수정.
        self.assertRedirects(response, '/lists/only_one_list_in_the_world/')
