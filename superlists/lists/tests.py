from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from .views import home_page


# Create your tests here.
# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        # resolve('/') : 장고의 내부함수로 url을 해석해서 일치하는 뷰함수를 찾는다.
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # HttpRequest 객체를 생성해 어떤 요청을 브라우저에 보내는지 확인
        request = HttpRequest()
        # home_page 뷰에 전달해서 HttpResponse 객체로 응답을 받는다.
        response = home_page(request)
        # byte형 데이터인 <html></html>로 구성되어 있는지 확인
        self.assertTrue(response.content.startswith(b'<html>'))
        # title에 특정 단어가 있는지 확인
        self.assertIn(b'<title>To Do Lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
