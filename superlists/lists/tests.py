from django.core.urlresolvers import resolve
from django.test import TestCase

from .views import home_page


# Create your tests here.
# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)


class HomePageTest(TestCase):
    def test_root_url_resolves_to_homepage_view(self):
        # resolve('/') : 장고의 내부함수로 url을 해석해서 일치하는 뷰함수를 찾는다.
        found = resolve('/')
        self.assertEqual(found.func, home_page)
