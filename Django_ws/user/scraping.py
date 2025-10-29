from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

def scraping(studentId, studentPW):
    try:
        options = webdriver.ChromeOptions()
        
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])

        driver = webdriver.Chrome(options = options)
        driver.get('https://info.cku.ac.kr/haksa/common/loginForm2.jsp')
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH, '//area[@title="통합로그인"]').click()
        driver.implicitly_wait(2)

        ckuID = driver.find_element(By.ID, 'login_id')
        ckuID.send_keys(studentId)
        ckuPW = driver.find_element(By.ID, 'login_pwd')
        ckuPW.send_keys(studentPW)
        driver.find_element(By.XPATH, '//a[@class="login"]').click()
        driver.implicitly_wait(2)

        driver.find_element(By.XPATH, '//a[@class="snbmenu1"]').click()
        driver.find_element(By.XPATH, '//a[text()="전체 성적조회"]').click()

        student_id = driver.find_element(By.XPATH, '//th[text()="학번"]/following-sibling::td[1]').text
        name = driver.find_element(By.XPATH, '//th[text()="성명"]/following-sibling::td[1]').text
        major = driver.find_element(By.XPATH, '//th[text()="소속"]/following-sibling::td[1]').text[:-3]
        driver.quit()
        return student_id, name, major

    except UnexpectedAlertPresentException:
        driver.quit()
        errorMessage = '아이디 또는 비밀번호를 확인해주세요.'
        return errorMessage
    except Exception as e:
        driver.quit()
        print(f'재학생 인증 오류코드(디버깅): {e}')
        errorMessage = '회원정보 형식이 일치하지 않습니다. 관리자에게 문의하세요.'
        return errorMessage
