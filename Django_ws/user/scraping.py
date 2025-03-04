from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from bs4 import BeautifulSoup

def scraping(studentId, studentPW):
    try:
        options = webdriver.ChromeOptions()
        
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])

        driver = webdriver.Chrome(options = options)
        driver.get('https://info.cku.ac.kr/haksa/common/loginForm2.jsp')
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, '//area[@title="통합로그인"]').click()
        driver.implicitly_wait(1)

        ckuID = driver.find_element(By.ID, 'login_id')
        ckuID.send_keys(studentId)
        ckuPW = driver.find_element(By.ID, 'login_pwd')
        ckuPW.send_keys(studentPW)
        driver.find_element(By.XPATH, '//a[@class="login"]').click()
        driver.implicitly_wait(1)

        driver.find_element(By.XPATH, '//a[@class="snbmenu1"]').click()
        driver.find_element(By.XPATH, '//a[text()="학생신상기록카드조회"]').click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        student_id = soup.find('td', class_='num').text
        name = soup.find('th', class_='pad_3').find_previous_sibling('td').text
        major, grade = soup.find('th', string='학과/학년').find_next('td').text.split()

        return student_id, name, major
    except UnexpectedAlertPresentException:
        driver.quit()
        errorMessage = '아이디 또는 비밀번호를 확인해주세요.'
        return errorMessage
    except:
        driver.quit()
        errorMessage = '회원 정보를 확인할 수 없습니다. 잠시 후 다시 시도해주세요.'
        return errorMessage