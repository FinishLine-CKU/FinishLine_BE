"""
원클릭 검사 부하 테스트용 더미 User를 생성/삭제한다.

oneclick_test API는 studentId로 User.major를 조회해 save_pdf_data_to_db에 넘기므로,
DB에 없는 학번으로 부하 테스트를 하면 major=None 분기만 타서
(특히 '사제동행세미나' 매칭 경로) 운영 부담을 그대로 재현하지 못한다.
docs/oneclick_load_test.md 참고.

학번은 docs/loadtest(save_db 측정용)와 같은 YYYY90NN 형식을 쓰되,
그쪽 01~10과 겹치지 않도록 NN=11부터 생성한다. (최대 89명)

사용법:
    python manage.py seed_load_test_users --count 50
    python manage.py seed_load_test_users --count 50 --year 2022 --major-code CS01
    python manage.py seed_load_test_users --delete
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from user.models import MajorMap, User

NAME_PREFIX = "부하테스트"
START_NO = 11
MAX_COUNT = 100 - START_NO


def make_student_id(year, i):
    return f"{year}90{START_NO + i:02d}"


class Command(BaseCommand):
    help = "부하 테스트용 더미 User(학번 YYYY9011~)를 생성하거나 삭제한다."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=50, help=f"생성할 더미 User 수 (최대 {MAX_COUNT})")
        parser.add_argument("--year", type=str, default="2022", help="학번 앞 4자리(입학년도)")
        parser.add_argument("--major-code", type=str, default=None, help="부여할 MajorMap.major_code (미지정 시 첫 번째 MajorMap 사용)")
        parser.add_argument("--delete", action="store_true", help="부하테스트 더미 User를 전부 삭제")

    def handle(self, *args, **options):
        if options["delete"]:
            deleted, _ = User.objects.filter(
                name__startswith=NAME_PREFIX, student_id__regex=r"^[0-9]{4}90[0-9]{2}$"
            ).delete()
            self.stdout.write(self.style.SUCCESS(f"삭제 완료: {deleted}건"))
            return

        major_code = options["major_code"]
        if not major_code:
            major_map = MajorMap.objects.first()
            if not major_map:
                raise CommandError("MajorMap에 데이터가 없습니다. --major-code로 직접 지정해주세요.")
            major_code = major_map.major_code

        count = options["count"]
        if not 1 <= count <= MAX_COUNT:
            raise CommandError(f"--count는 1~{MAX_COUNT} 사이여야 합니다.")
        year = options["year"]
        now = timezone.now()
        created = 0

        for i in range(count):
            student_id = make_student_id(year, i)
            _, was_created = User.objects.update_or_create(
                student_id=student_id,
                defaults={
                    "name": f"{NAME_PREFIX}{START_NO + i:02d}",
                    "password": "loadtest",
                    "major": major_code,
                    "date_time_joined": now,
                },
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f"완료: 총 {count}건 처리(신규 {created}건), major_code={major_code}, "
            f"학번 {make_student_id(year, 0)}~{make_student_id(year, count - 1)}"
        ))
