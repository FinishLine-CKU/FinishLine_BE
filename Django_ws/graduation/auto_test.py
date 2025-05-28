from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

def auto_test(studentId, studentPW):
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

        rows = driver.find_elements(By.XPATH, '//div[@class="dataArea"]/table[3]/tbody/tr')

        lectures_data = []

        for row in rows:
            year, semester = row.find_element(By.XPATH, './td[1]').text.split('/')  # 이수학기
            area = row.find_element(By.XPATH, './td[2]').text  # 이수구분
            topic = row.find_element(By.XPATH, './td[3]').text  # 이수영역/주제
            lecture_name = row.find_element(By.XPATH, './td[4]').text  # 교과목명
            credit = row.find_element(By.XPATH, './td[5]').text  # 학점
            grade = row.find_element(By.XPATH, './td[6]').text  # 등급

            if grade == 'N' or grade == 'F':
                continue
            

            if area == '전공필수':
                area = '전필'
            elif area == '전공선택':
                area = '전선'
            elif area == '교양필수':
                area = '교필'
            elif area == '교양선택':
                area = '교선'
            elif area == '일반선택':
                area = '일선'
            elif area == '소단위전공':
                area = '소전'
            elif area == '복수전공':
                area = '복전'
            elif area == '부전공':
                area = '부전'
            elif area == '연계전공':
                area = '연계'
            elif area == '전공기초':
                area = '전기'
            elif area == '전공심화':
                area = '전심'
            elif area == '전공기초':
                area = '전기'
            elif area == '공통전공':
                area = '공통'

            subject_data = {
                '이수년도': year,
                '학기': semester,
                '이수구분': area,
                '주제': topic if topic else ' ',
                '교과목명': lecture_name,
                '학점': credit,
                '학번': studentId
            }

            lectures_data.append(subject_data)

        driver.quit()

        return lectures_data

    except UnexpectedAlertPresentException:
        driver.quit()
        errorMessage = '아이디 또는 비밀번호를 확인해주세요.'
        return errorMessage

    except Exception as e:
        driver.quit()
        print(f'원클릭 검사 크롤링 오류코드(디버깅): {e}')
        errorMessage = '회원 정보를 확인할 수 없습니다. 잠시 후 다시 시도해주세요.'
        # 로그인 오류 or 크롤링 오류
        return errorMessage