from django.core.management.base import BaseCommand
from graduation.testdb import upload_alllecture_data  # 위에서 작성한 함수 임포트

class Command(BaseCommand):
    help = '엑셀 파일을 읽고 데이터를 DB에 저장'

    def handle(self, *args, **kwargs):
        # upload_from_media 함수 실행
        upload_alllecture_data()
        self.stdout.write(self.style.SUCCESS('엑셀 데이터가 DB에 성공적으로 저장되었습니다.'))