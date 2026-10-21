"""
원클릭 검사(oneclick_test) 부하 테스트 스크립트.
docs/oneclick_load_test.md 참고.

사전 준비:
  1) 대상 서버에서 mock_portal 실행 후 auto_test.py가 이를 보도록
     CKU_PORTAL_BASE_URL=http://127.0.0.1:8888 로 Django 서버 기동
  2) python manage.py seed_load_test_users --count <동시 사용자 수 이상>
     으로 LOADTEST0000~ 학번의 더미 User 생성

실행:
  pip install -r load_test/requirements.txt
  locust -f load_test/locustfile.py --host https://<테스트 대상 서버>

  헤드리스 예시(동시 사용자 20명, 초당 2명씩 증가, 3분간):
  locust -f load_test/locustfile.py --host https://<테스트 대상 서버> \
      --headless -u 20 -r 2 -t 3m --csv=load_test/result
"""
import itertools

from locust import HttpUser, task, between

# seed_load_test_users.py가 생성하는 학번과 동일한 규칙(LOADTEST0000~)
_student_id_counter = itertools.count()


class OneClickUser(HttpUser):
    # auto_test 자체가 8~10s 걸리는 무거운 동작이므로, 사용자가 결과를 보고
    # 재시도하기까지의 대기시간을 짧게 잡아 동시 접속 부하를 유지한다.
    wait_time = between(1, 3)

    def on_start(self):
        self.student_id = f"LOADTEST{next(_student_id_counter) % 9999:04d}"

    @task
    def oneclick_test(self):
        self.client.post(
            "/graduation/oneclick_test/",
            json={"studentId": self.student_id, "studentPW": "loadtest"},
            name="/graduation/oneclick_test/",
        )
