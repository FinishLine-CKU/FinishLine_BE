"""
원클릭 검사 부하 테스트용 가짜 가톨릭관동대 포털 서버.

실제 외부 시스템(info.cku.ac.kr)에 부하 테스트 트래픽을 보낼 수 없는 상태에서,
graduation/auto_test.py(Selenium)가 요구하는 페이지 흐름
(로그인 폼 -> 로그인 -> 학사정보 메뉴 -> 하위메뉴 -> 전체 성적조회)을 재현한다.
자세한 배경은 docs/oneclick_load_test.md 참고.

실행:
    python load_test/mock_portal/server.py

환경변수:
    MOCK_PORTAL_PORT   서버 포트 (기본 8888)
    MOCK_PORTAL_DELAY  페이지 1건당 인위적 지연(초, 기본 0.2)
                        -> 테스트 EC2에서 auto_test 약 9s로, 운영에서 관측되는
                           auto_test 평균 소요(8~10s)를 재현하기 위한 값 (1.6에서 보정)

auto_test.py가 이 서버를 보게 하려면:
    CKU_PORTAL_BASE_URL=http://127.0.0.1:8888

학번별 성적 페이지:
    로그인 시 입력한 학번이 쿠키(mock_sid)로 전달된다. 학번이 YYYY90NN(NN>=11)이면
    pages/grades/profiles/{(NN-11) % 프로필 수 + 1:02d}.html 을 돌려준다.
    (프로필 페이지는 generate_grades_page.py --profiles <json>으로 생성)
    그 외 학번이거나 프로필 페이지가 없으면 기존 grades.html(60과목)을 돌려준다.
"""
import os
import re
import time
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PAGES_DIR = Path(__file__).parent / "pages"
PORT = int(os.environ.get("MOCK_PORTAL_PORT", "8888"))
PAGE_DELAY_SECONDS = float(os.environ.get("MOCK_PORTAL_DELAY", "0.2"))
PROFILES_DIR = PAGES_DIR / "grades" / "profiles"
PROFILE_PAGES = sorted(PROFILES_DIR.glob("*.html"))
LOADTEST_ID = re.compile(r"^\d{4}90(\d{2})$")

ROUTES = {
    "/haksa/common/loginForm2.jsp": PAGES_DIR / "haksa/common/loginForm2.jsp",
    "/login/login_page.html": PAGES_DIR / "login/login_page.html",
    "/menu/menu_main.html": PAGES_DIR / "menu/menu_main.html",
    "/menu/menu_sub.html": PAGES_DIR / "menu/menu_sub.html",
    "/grades/grades.html": PAGES_DIR / "grades/grades.html",
}


def profile_page(cookie_header):
    morsel = SimpleCookie(cookie_header or "").get("mock_sid")
    match = LOADTEST_ID.match(morsel.value) if morsel else None
    if not match or int(match.group(1)) < 11 or not PROFILE_PAGES:
        return None
    return PROFILE_PAGES[(int(match.group(1)) - 11) % len(PROFILE_PAGES)]


class MockPortalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        file_path = ROUTES.get(path)
        if path == "/grades/grades.html":
            file_path = profile_page(self.headers.get("Cookie")) or file_path

        if file_path is None or not file_path.exists():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        time.sleep(PAGE_DELAY_SECONDS)

        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # 부하 테스트 중 대량 접속 로그를 남기지 않는다.


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), MockPortalHandler)
    print(f"[mock_portal] listening on 0.0.0.0:{PORT} (delay={PAGE_DELAY_SECONDS}s/page, profiles={len(PROFILE_PAGES)})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
