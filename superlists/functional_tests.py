import unittest

from selenium import webdriver


# unittest 모듈의 TestCase 상속
class NewVisitorTest(unittest.TestCase):
    # 테스트 시작시 실행 - 크롬브라우저를 열고 3초 대기한 후 테스트 코드 실행
    def setUp(self):
        self.browser = webdriver.Chrome()
        # 암묵적 대기 기능 추가 - 3초 대기 후 처리
        self.browser.implicitly_wait(3)

    # 테스트 종료시 실행 - 자동으로 창 닫아준다.
    def tearDown(self):
        self.browser.quit()

    # 테스트 메인코드
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # unittest의 내장함수 사용
        self.assertIn('To-do', self.browser.title)
        # 강제 테스트 실패를 발생시켜 에러메세지를 출력한다.
        # 일반적으로 테스트가 끝난 것을 알기 위해 넣는다.
        self.fail('Finish the test!')


if __name__ == '__main__':
    # 테스트 작성시 발생하는 불필요한 리소스 경고를 제거
    unittest.main(warnings='ignore')
