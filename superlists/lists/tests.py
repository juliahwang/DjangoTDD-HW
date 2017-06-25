import re

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from .models import Item, List
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


class ListAndItemModelsTest(TestCase):
    pattern_input_csrf = re.compile(r'<input[^>]*csrfmiddlewaretoken[^>]*>')

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'lists/list.html')

    # 템플릿이 여러 아이템을 출력할 수 있는지 확인하는 테스트
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        # 장고의 TestCase 속성을 사용(self.client)
        # 여기에 테스트할 URL을 .get한다.
        response = self.client.get('/lists/{}/'.format(correct_list.id))

        # 응답내용 처리를 자동으로 해주는 장고의 assertContains 메서드 사용
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/list/{}/'.format(correct_list.id))
        # self.assertEqual(response.context['list'], correct_list)


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
        new_list = List.objects.first()
        # 응답이 html 에 의해 렌더링되지 않고 redirect되므로 이를 확인하는 코드로 수정.
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))

    # 기존 목록에 아이템을 추가하기 위한 또 다른 뷰
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={
                'item_text': '기존 목록에 신규 아이템',
            }
        )
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '기존 목록에 신규 아이템')
        self.assertEqual(new_item.list, correct_list)
        
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={
                'item_text': '기존 목록에 신규 아이템',
            }
        )
        
        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))