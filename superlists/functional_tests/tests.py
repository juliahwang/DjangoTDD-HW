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
        # self.assertIn('To-Do', header_text)

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
        user1_list_url = self.browser.current_url
        # unittest의 헬퍼메서드, 정규표현과 문자열이 일치하는지 확인해줌
        self.assertRegex(user1_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: 개발공부하기')

        # 추가 아이템을 입력할 수 있는 여분 텍스트 상자가 보여야 한다.
        # 사용자는 아이템을 또 추가한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('숙제도 하기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지가 업데이트되고 난 후에 추가한 아이템 2개가 여전히 있는지 확인
        self.check_for_row_in_list_table('1: 개발공부하기')
        self.check_for_row_in_list_table('2: 숙제도 하기')

        # + 코드 추가 - 사용자마다 url이 부여되는가?
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 사용자2가 홈페이지에 접속하면 사용자1의 리스트는 보이지 않는다
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('개발공부하기', page_text)
        self.assertNotIn('숙제도 하기', page_text)

        # 사용자2가 새로운 아이템을 입력한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        # 사용자2가 자신만의 전용 URL을 획득한다.
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)

        # 사용자1이 입력한 흔적이 없다는 것을 확인한다.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('개발공부하기', page_text)
        self.assertIn('우유 사기', page_text)


### 장고 테스트 실행자를 사용하기 때문에 더이상 필요 없음
# if __name__ == '__main__':
#     # 테스트 작성시 발생하는 불필요한 리소스 경고를 제거
#     unittest.main(warnings='ignore')
