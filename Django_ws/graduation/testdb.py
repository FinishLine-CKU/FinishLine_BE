import os
import pandas as pd
from django.conf import settings
from graduation.models import AllLectureData  # 저장할 모델 가져오기
from graduation.models import NowLectureData  # 저장할 모델 가져오기

def upload_alllecture_data():
    # 엑셀 파일 경로 지정
    file_path = os.path.join(settings.MEDIA_ROOT, 'nodulip.xlsx')  # 파일 이름과 경로 설정

    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path)

        # 데이터 확인 및 저장
        for _, row in df.iterrows():
            try:
                # 데이터베이스에 직접 저장 (중복 확인 없이)
                NowLectureData.objects.create(
                    year=row['개설년도'],                     # 엑셀의 '개설년도' 열
                    semester=row['학기'],                   # 엑셀의 '학기' 열
                    lecture_code=row['교과목코드'],           # 엑셀의 '교과목코드' 열
                    lecture_name=row['교과목명'],           # 엑셀의 '교과목명' 열
                    lecture_type=row['이수구분'],           # 엑셀의 '이수구분' 열
                    lecture_topic=row.get('이수영역', ' '),  # 엑셀의 '이수영역' 열 (없으면 빈 값)
                    credit=row.get('학점', 0.0),            # '학점' 열 (없으면 0.0)
                    major_code=row.get('전공코드', ' ')       # 'value' 열 (없으면 빈 값)
                )
                # print(f"Added lecture: {row['교과목명']}")
            except Exception as e:
                print(f"Error processing row: {row.to_dict()}, Error: {str(e)}")
    except Exception as e:
        print(f"Error reading file: {file_path}, Error: {str(e)}")