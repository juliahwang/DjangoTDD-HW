import unittest

from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


# unittest 모듈의 TestCase 상속
class NewVisitorTest(LiveServerTestCase):
    # 테스트 시작시 실행 - 크롬브라우저를 열고 3초 대기한 후 테스트 코드 실행
    def setUp(self):
        self.browser = webdriver.Chrome()
        # 암묵적 대기 기능 추가 - 3초 대기 후 처리
        self.browser.implicitly_wait(3)

    # 테스트 종료시 실행 - 자동으로 창 닫아준다.
    def tearDown(self):
        self.browser.quit()

    # 동일코드의 반복을 줄이기 위해 헬퍼 메서드로 정의
    # - 'test_'로 시작하지 않으면 테스트 실행시 자동으로 실행되지 않는다!!
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # 테스트 메인코드
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 사용자는 앱을 켠다 - LiveServerTestCase의 속성 사용
        self.browser.get(self.live_server_url)

        # unittest의 내장함수 사용
        # 웹페이지 타이틀과 헤더가 'To-Do'를 표시하고 있다
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 사용자는 작업을 추가해본다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력',
        )

        # 사용자는 '개발공부하기'라고 텍스트 상자에 입력한다.
        inputbox.send_keys('개발공부하기')

        # enter키를 치면 페이지 갱신과 동시에 작업목록에 아이템이 추가된다.
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: 개발공부하기')

        # 추가 아이템을 입력할 수 있는 여분 텍스트 상자가 보여야 한다.
        # 사용자는 아이템을 또 추가한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('숙제도 하기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지가 업데이트되고 난 후에 추가한 아이템 2개가 여전히 있는지 확인
        self.check_for_row_in_list_table('1: 개발공부하기')
        self.check_for_row_in_list_table('2: 숙제도 하기')

        # 기능테스트 디버깅 - 실행시간 늘이기
        # import time
        # time.sleep(5)
        # 페이지가 갱신되고 2개의 아이템이 목록에 보인다.
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: 개발공부하기', [row.text for row in rows])
        self.assertIn(
            '2: 숙제도 하기',
            [row.text for row in rows]
        )

        # 강제 테스트 실패를 발생시켜 에러메세지를 출력한다.
        # 일반적으로 테스트가 끝난 것을 알기 위해 넣는다.
        self.fail('Finish the test!')


### 장고 테스트 실행자를 사용하기 때문에 더이상 필요 없음
# if __name__ == '__main__':
#     # 테스트 작성시 발생하는 불필요한 리소스 경고를 제거
#     unittest.main(warnings='ignore')