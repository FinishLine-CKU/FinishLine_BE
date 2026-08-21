# 26년도 교양 계산 로직 (신규)
# 23~25년도 트리니티 구조(인성/기초/융합)와 달리, 26년도는 단과대 구분 없이
# 교양 필수(VERUM인성, VERUM인간, 디지털소통, 디지털시대의사고와표현) + 교양 선택(12개 주제 중 16학점)으로 구성된다.
# 신규 마이그레이션 없이 기존 GEStandard 필드를 재사용한다.
#   - 필수 : 인간학(VERUM인간), VERUM캠프(VERUM인성), 논리적사고와글쓰기(디지털시대의사고와표현), 디지털소통
#   - 선택 : 자기관리(진로탐색, 창의성, 창업) / 융합비고(정치와경제, 심리와건강, 정보와기술, 인간과문학, 역사와사회, 철학과예술, 자연과환경, 수리와과학, 언어와문화)
#           (23~25년과 달리 택1 제한 없이 자유롭게 합산)

from decimal import Decimal
from user.models import User
from .models import MyDoneLecture
from .models import GEStandard
from .GE_calculate import calculate_and_save_standard
from .micro_degree_calculate import select_user_standard

# 자기관리로 묶이는 주제 (택1 제한 없이 자유 합산)
CAREER_TOPICS = ['진로탐색', '창의성', '창업']

# 융합비고로 묶이는 주제 (택1 제한 없이 자유 합산)
FUSION_NOTE_TOPICS = ['정치와경제', '심리와건강', '정보와기술', '인간과문학', '역사와사회', '철학과예술', '자연과환경', '수리와과학', '언어와문화']


# 26년도 교양 이수학점 계산
def get_user_GE_2026(user_id):
    mydone_lecture_list = MyDoneLecture.objects.filter(user_id=user_id, lecture_type__in=['교양', '교선', '교필'])
    lectures_dict = []
    done_GE = Decimal('0.0')

    for lecture in mydone_lecture_list:
        lecture_data = {
            '교과목명': lecture.lecture_name,
            '주제': lecture.lecture_topic,
            '학점': lecture.credit
            }
        lectures_dict.append(lecture_data)

    # 26학년도 대체 교과목 전처리 (기존 get_user_GE()와 동일한 주제 매핑)
    for lecture in lectures_dict:
        if lecture['주제'] == 'VERUM인간':
            lecture['주제'] = '인간학'

        elif lecture['주제'] == 'VERUM인성':
            lecture['주제'] = 'VERUM캠프'

        elif lecture['주제'] == '디지털시대의사고와표현':
            lecture['주제'] = '논리적사고와글쓰기'

    for data in lectures_dict:
        done_GE += data['학점']  # 교양과목 총 이수 학점

    return lectures_dict, done_GE


# 26년도 교양 졸업요건 추출 (단과대 구분 없이 공통)
def get_user_GE_standard_2026():
    filtered_data = GEStandard.objects.filter(연도='2026').values()

    if not filtered_data:
        print(f"GEStandard_id can not found")

    essential_GE_data = {'인간학', 'VERUM캠프', '논리적사고와글쓰기', '디지털소통'}
    choice_GE_data = {'자기관리', '융합비고'}

    cleaned_data = [
        {key: value for key, value in item.items() if key not in ['GEStandard_id', '연도'] and value != 0}
        for item in filtered_data
    ]

    essential_GE_standard = [
        {key: value for key, value in item.items() if key in essential_GE_data}
        for item in cleaned_data
    ]

    choice_GE_standard = [
        {key: value for key, value in item.items() if key in choice_GE_data}
        for item in cleaned_data
    ]

    for item in essential_GE_standard:
        total_sum = sum(Decimal(value) for value in item.values())
        item['총합'] = total_sum

    for item in choice_GE_standard:
        total_sum = sum(Decimal(value) for value in item.values())
        item['총합'] = total_sum

    return {"essential_GE_standard": essential_GE_standard,
            "choice_GE_standard": choice_GE_standard}


# 26년도 교양 필수 계산 (인간학, VERUM캠프, 논리적사고와글쓰기, 디지털소통)
def GE_essential_calculate_2026(lecture_dict, user_GE_standard):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['essential_GE_standard']
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = Decimal('0.0')

    lecture_check = []

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        for GE_standard in user_GE_standard:
            if lecture_topic in GE_standard:
                lecture_update = needcheck
                GE_credit = GE_standard[lecture_topic]

                if lecture_credit < GE_credit:
                    missing_credit = GE_credit - lecture_credit
                    GE_standard[lecture_topic] = missing_credit

                    delete_items.append(needcheck)

                    GE_standard['총합'] -= lecture_credit

                    lecture_update['분류'] = lecture_topic
                    lecture_check.append(lecture_update)

                elif lecture_credit > GE_credit:
                    del GE_standard[lecture_topic]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)

                    delete_items.append(needcheck)

                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))

                    lecture_update['분류'] = lecture_topic
                    lecture_check.append(lecture_update)

                elif lecture_credit == GE_credit:
                    del GE_standard[lecture_topic]
                    GE_standard['총합'] -= GE_credit

                    delete_items.append(needcheck)

                    lecture_update['분류'] = lecture_topic
                    lecture_check.append(lecture_update)

            else:
                break

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

    return lectures_dict, user_GE_standard, rest_total, lecture_check


# 26년도 교양 선택 계산 (자기관리: 진로탐색/창의성/창업, 융합비고: 9개 주제) - 택1 제한 없이 자유 합산
def GE_choice_calculate_2026(lecture_dict, user_GE_standard, rest_total):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['choice_GE_standard']
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = rest_total

    lecture_check = []

    # 부족 영역 표시용 - 이미 이수한 주제 기록 (GE_calculate_trinity.py의 stack_search 등과 동일한 목적)
    stack_career = []
    stack_fusion_note = []

    #진로탐색, 창의성, 창업 → 자기관리
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in CAREER_TOPICS:

            if lecture_topic not in stack_career:
                stack_career.append(lecture_topic)

            for GE_standard in user_GE_standard:
                if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                    lecture_update = needcheck
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["자기관리"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '자기관리'
                    lecture_check.append(lecture_update)

                elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit:
                    lecture_update = needcheck
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '자기관리'
                    lecture_check.append(lecture_update)

                elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit:
                    lecture_update = needcheck
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)

                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = '자기관리'
                    lecture_check.append(lecture_update)

                else:
                    break

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #정치와경제, 심리와건강, 정보와기술, 인간과문학, 역사와사회, 철학과예술, 자연과환경, 수리와과학, 언어와문화 → 융합비고
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in FUSION_NOTE_TOPICS:

            if lecture_topic not in stack_fusion_note:
                stack_fusion_note.append(lecture_topic)

            for GE_standard in user_GE_standard:
                if "융합비고" in GE_standard and GE_standard["융합비고"] > lecture_credit:
                    lecture_update = needcheck
                    GE_credit = GE_standard["융합비고"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["융합비고"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '융합비고'
                    lecture_check.append(lecture_update)

                elif "융합비고" in GE_standard and GE_standard["융합비고"] == lecture_credit:
                    lecture_update = needcheck
                    del GE_standard["융합비고"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '융합비고'
                    lecture_check.append(lecture_update)

                elif "융합비고" in GE_standard and GE_standard["융합비고"] < lecture_credit:
                    lecture_update = needcheck
                    GE_credit = GE_standard["융합비고"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["융합비고"]
                    delete_items.append(needcheck)

                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = '융합비고'
                    lecture_check.append(lecture_update)

                else:
                    break

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

    return lectures_dict, user_GE_standard, rest_total, lecture_check, stack_career, stack_fusion_note


#일반선택 학점 계산 (교양 계산 후 남은 교과목으로 일반선택 이수 학점 계산)
def rest_and_done_calculate_2026(lecture_dict_result, rest_total):
    rest_total_last = Decimal('0.0')
    for item in lecture_dict_result:
        rest_total_last += item['학점']

    rest_total_topic = rest_total_last + rest_total

    return rest_total_topic


#26년도 교양 계산 컨트롤타워
def GE_2026_calculate(user_id):
    #전체과목 데이터 추출
    lecture_dict, done_GE = get_user_GE_2026(user_id)

    #사용자 교양요건 추출
    user_GE_standard = get_user_GE_standard_2026()

    print(f"교양 필수 기준: {user_GE_standard['essential_GE_standard'][0]}")
    print(f"교양 선택 기준: {user_GE_standard['choice_GE_standard'][0]}")

    lecture_dict_result, essential_standard, rest_total, essential_lecture_check = GE_essential_calculate_2026(lecture_dict, user_GE_standard)

    lecture_dict_result, choice_standard, rest_total, choice_lecture_check, stack_career, stack_fusion_note = GE_choice_calculate_2026(lecture_dict_result, user_GE_standard, rest_total)

    #일반선택 학점 계산
    rest_total = rest_and_done_calculate_2026(lecture_dict_result, rest_total)

    print(f"부족 영역(교양 필수): {essential_standard[0]}")
    print(f"부족 영역(교양 선택): {choice_standard[0]}")
    print(f'교양 > 일선 학점: {rest_total}\n')

    #교양 부족 학점
    lack_essential_total = essential_standard[0]['총합']
    lack_choice_total = choice_standard[0]['총합']

    lack_essential_topic = essential_standard[0]
    lack_choice_topic = choice_standard[0]

    #총합 제거
    lack_essential_topic.pop('총합')
    lack_choice_topic.pop('총합')

    #교양 선택 소분류 제목으로 변경 - 이미 이수한 주제는 표시에서 제외
    changed_lack_choice_topic = {}
    for key in lack_choice_topic:
        if key == '자기관리':
            topic = [t for t in CAREER_TOPICS if t not in stack_career]
            new_key = ', '.join(topic) if topic else ', '.join(CAREER_TOPICS)
            changed_lack_choice_topic[new_key] = lack_choice_topic[key]

        elif key == '융합비고':
            topic = [t for t in FUSION_NOTE_TOPICS if t not in stack_fusion_note]
            new_key = ', '.join(topic) if topic else ', '.join(FUSION_NOTE_TOPICS)
            changed_lack_choice_topic[new_key] = lack_choice_topic[key]

        else:
            changed_lack_choice_topic[key] = lack_choice_topic[key]

    #DB에 저장할 교양 이수 학점, 교양 부족 학점, 일반선택 학점, 학번
    done_essential_GE = sum(Decimal(item['학점']) for item in essential_lecture_check)
    done_choice_GE = sum(Decimal(item['학점']) for item in choice_lecture_check)

    lack_total_GE = lack_essential_total + lack_choice_total

    #DB에 저장할 교양 세부 검사 과정
    GE_lecture_check = essential_lecture_check + choice_lecture_check

    #DB에 저장
    calculate_and_save_standard(done_GE, lack_total_GE, rest_total, user_id, GE_lecture_check)

    data = {
            'lackEssentialGE': lack_essential_total + lack_choice_total,
            'lackChoiceGE': None,

            'lackEssentialGETopic': lack_essential_topic | changed_lack_choice_topic,
            'lackChoiceGETopic': None,

            'doneEssentialGE': done_essential_GE + done_choice_GE,
            'doneChoiceGE': None,

            'doneGERest': rest_total,
    }

    return data


# 26년도 교양 상세 정보 조회 (ge_detail_view)
# 23~25년 트리니티 구조와 표 형태가 달라 GE_detail_check.py의 기존 로직을 재사용할 수 없어 신규 작성.
# 교양필수는 대표역량(공동체/소통·공감)별 개별 주제 기준을 그대로 보여주고,
# 교양선택은 자기관리/융합비고가 택1 제한 없이 자유 합산되는 구조이므로
# GE_detail_check.py의 트리니티 융합 표(정보활용/창의융합/문제해결 등 여러 주제 → 단일 기준 field)와 동일하게
# 자기관리(진로탐색/창의성/창업), 융합비고(9개 주제)를 각각 하나의 대표역량 행으로 묶어서 보여준다.
def GE_detail_check_2026(user_id):
    user_major = User.objects.filter(student_id=user_id).values('major').first()
    MD_standard, rest_standard = select_user_standard(user_id)

    data = get_user_GE_standard_2026()

    essentialTable = []
    choiceTable = []
    rest_list = []
    success_count_1 = Decimal('0.0')
    success_count_2 = Decimal('0.0')

    my_list = list(
        MyDoneLecture.objects.filter(user_id=user_id)
        .values('year', 'semester', 'lecture_name', 'lecture_type', 'credit', 'lecture_topic', 'matched_topic')
    )

    for item in my_list:
        item['year'] = item['year'][2:]

    #####교양필수 (공동체 : VERUM캠프, 인간학 / 소통·공감 : 디지털소통, 논리적사고와글쓰기)#####
    essential_order = ['VERUM캠프', '인간학', '디지털소통', '논리적사고와글쓰기']

    for ordered in essential_order:
        for item in data['essential_GE_standard']:
            if ordered in item:
                essentialTable.append({
                    "topic": ordered,
                    "standard": item[ordered],
                    "subject": []
                })

    for item in my_list:
        if item['matched_topic'] in essential_order:
            for i in essentialTable:
                if i['topic'] == item['matched_topic']:
                    i['subject'].append(item)
                    success_count_1 += item['credit']

    if success_count_1 >= data['essential_GE_standard'][0]['총합']:
        essentialTable.append({"success": True})
    else:
        essentialTable.append({"success": False})

    # 계산용 내부 topic 명칭(GEStandard 컬럼명/matched_topic 매칭 키)과 2026 화면 표시명이 달라
    # 매칭이 끝난 뒤 표시용 라벨만 치환한다(계산 로직에는 영향 없음).
    essential_display_label = {
        'VERUM캠프': 'VERUM인성',
        '인간학': 'VERUM인간',
        '논리적사고와글쓰기': '디지털시대의사고와표현',
    }
    for i in essentialTable:
        if 'topic' in i and i['topic'] in essential_display_label:
            i['topic'] = essential_display_label[i['topic']]

    #####교양선택 (미래설계 : 자기관리 / 디지털융합·지역혁신·지속가능발전 : 융합비고)#####
    career_topic_label = ','.join(CAREER_TOPICS)
    fusion_topic_label = ','.join(FUSION_NOTE_TOPICS)

    for item in data['choice_GE_standard']:
        if '자기관리' in item:
            choiceTable.append({
                "topic": career_topic_label,
                "standard": item['자기관리'],
                "subject": []
            })
        if '융합비고' in item:
            choiceTable.append({
                "topic": fusion_topic_label,
                "standard": item['융합비고'],
                "subject": []
            })

    for item in my_list:
        if item['matched_topic'] == '자기관리':
            for i in choiceTable:
                if i['topic'] == career_topic_label:
                    i['subject'].append(item)
                    success_count_2 += item['credit']

        elif item['matched_topic'] == '융합비고':
            for i in choiceTable:
                if i['topic'] == fusion_topic_label:
                    i['subject'].append(item)
                    success_count_2 += item['credit']

    if success_count_2 >= data['choice_GE_standard'][0]['총합']:
        choiceTable.append({"success": True})
    else:
        choiceTable.append({"success": False})

    #####일반선택#####
    for item in my_list:
        if item['matched_topic'] == '일반선택':
            rest_list.append(item)

    restTable = {
        "topic": "일반선택",
        "standard": rest_standard,
        "subject": rest_list
    }

    print(f"Checked 2026 GE Detail Info! \n학번: {user_id} \n전공: {user_major}")

    return essentialTable, choiceTable, restTable
