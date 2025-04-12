from .models import MyDoneLecture
from .models import liberRequire
from decimal import Decimal

#사용자 소속 대학 추출
def are_you_human(user_major):
    human_service = ['032709*', '032708*', '032705*', '032703*', '032702*']
    medical_collage = ['030503*', '030501*', '030502*', '032801*', '032802*', '030702*', '030704*', '030705*', '030707*', '030709*', '030710*']
    user_home = user_major['major']

    if user_home in human_service:
        home_collage = '1' #휴먼서비스
    elif user_home in medical_collage:
        home_collage = '2' #의과, 헬스케어, 사범
    else:
        home_collage = '3' #일반

    return home_collage


#사용자 교양 이수학점 계산
def mydone_liber_get(user_id):
    student_id = user_id
    year = student_id[:4]

    mydone_lecture_list = MyDoneLecture.objects.filter(user_id=student_id, lecture_type__in=['교양', '교선', '교필'])
    lectures_dict = []
    complete_liber_total_credit = 0 #교양 총 학점
    complete_general_human_credit = 0 #교양 인성 총 학점
    complete_general_base_credit = 0 #교양 기초 총 학점
    complete_general_merge_credit = 0 #교양 융합 총 학점
    complete_general_esse_credit = 0 
    complete_general_choice_credit = 0

    for lecture in mydone_lecture_list:
        lecture_data = {
            '교과목명': lecture.lecture_name,
            '주제': lecture.lecture_topic,
            '학점': lecture.credit
            }
        lectures_dict.append(lecture_data)

    for less_item in lectures_dict:
        if less_item['주제'] == 'VERUM인성':
            less_item['주제'] = 'VERUM캠프'
    
    #트리니티라면
    if (year > '2022'):

        for data in lectures_dict[:]:
            complete_liber_total_credit += data['학점'] # 교양과목 총 이수 학점

        for data in lectures_dict[:]:
            if data['주제'] in {'VERUM캠프', '봉사활동', '인간학'}:
                complete_general_human_credit += data['학점']    # 교양인성 총 이수 학점
            elif data['주제'] in {'소통', '논리적사고와글쓰기', '외국어', '디지털소통', '자기관리', '진로탐색', '창의성', '창업', '계열기초'}:
                complete_general_base_credit += data['학점']  # 교양기초 총 이수 학점
            elif data['주제'] in {'정치와경제', '심리와건강', '정보와기술', '인간과문학', '역사와사회', '철학과예술', '자연과환경', '수리와과학', '언어와문화'}:
                complete_general_merge_credit += data['학점'] #교양융합 총 이수 학점

        data = {"complete_liber_total_credit": complete_liber_total_credit,
                "complete_general_human_credit": complete_general_human_credit, 
                "complete_general_base_credit": complete_general_base_credit,
                "complete_general_merge_credit": complete_general_merge_credit}
    
    #트리니티 이전이라면
    else:

        for data in lectures_dict[:]:
            complete_liber_total_credit += data['학점'] # 교양과목 총 이수 학점

        for data in lectures_dict[:]:
            if data['주제'] in {'인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', 'MSC교과군', '철학적인간학', '신학적인간학'}:
                complete_general_esse_credit += data['학점']    # 교양필수 총 이수 학점
            else:
                complete_general_choice_credit += data['학점']  # 교양선택 총 이수 학점

        data = {
            "complete_liber_total_credit": complete_liber_total_credit,
            "complete_general_esse_credit": complete_general_esse_credit,
            "complete_general_choice_credit": complete_general_choice_credit
        }

    return lectures_dict, data


#사용자 교양요건 추출
def user_liberrequire_get(year, home_collage):
    filtered_data = liberRequire.objects.filter(연도=year).values()
    if(int(year) > 2022):

        #교양인성
        if(home_collage == '1'):
            human_data = {'인간학'}
        elif(home_collage == '3' and year == '2023'):
            human_data = {'인간학', '트리니티아카데미'}
        else:
            human_data = {'인간학', '봉사활동', 'VERUM캠프'}

        #교양기초
        base_data = {'소통', '논리적사고와글쓰기', '외국어', '자기관리', '진로탐색', '창의성', '창업', '계열기초'}

        #교양융합
        if(year == '2025'):
            merge_data = {'정보활용', '창의융합', '문제해결', '융합비고'}
        else:
            merge_data = {'정보활용', '창의융합', '문제해결'}

        cleaned_data = [
            {key: value for key, value in item.items() if key not in ['liber_id', '연도'] and value != 0}
            for item in filtered_data
        ]
        human_result = [{key: value for key, value in item.items() if key in human_data} for item in cleaned_data]
        base_result = [{key: value for key, value in item.items() if key in base_data} for item in cleaned_data]
        merge_result = [{key: value for key, value in item.items() if key in merge_data} for item in cleaned_data]

        human_result = [
            {key: value for key, value in item.items() if key in human_data}
            for item in cleaned_data
        ]

        base_result = [
            {key: value for key, value in item.items() if key in base_data}
            for item in cleaned_data
        ]

        merge_result = [
            {key: value for key, value in item.items() if key in merge_data}
            for item in cleaned_data
        ]

        for item in human_result:
            total_sum = sum(Decimal(value) for value in item.values())  
            item['총합'] = total_sum 

        for item in base_result:
            total_sum = sum(Decimal(value) for value in item.values()) 
            item['총합'] = total_sum 

        for item in merge_result:
            total_sum = sum(Decimal(value) for value in item.values()) 
            item['총합'] = total_sum 

        data = {"human_result": human_result,
                "base_result": base_result,
                "merge_result": merge_result}

    else:
        # 교양필수 주제 (18 ~ 22년도 : 트리니티 이전)
        ness_data = {'인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', 'MSC교과군', '철학적인간학', '신학적인간학', 'VERUM인성'}
        
        # 교양선택 주제 (18 ~ 22년도 : 트리니티 이전)
        choice_data = {'고전탐구', '사유와지혜', '가치와실천', '상상력과표현', '인문융합', '균형1', '균형2', '균형3', '균형4', '계열기초'}
        
        cleaned_data = [
            {key: value for key, value in item.items() if key not in ['liber_id', '연도'] and value != 0}
            for item in filtered_data
        ]

        ness_result = [{key: value for key, value in item.items() if key in ness_data} for item in cleaned_data]
        choice_result = [{key: value for key, value in item.items() if key in choice_data} for item in cleaned_data]
        
        ness_result = [
            {key: value for key, value in item.items() if key in ness_data}
            for item in cleaned_data
        ]

        choice_result = [
            {key: value for key, value in item.items() if key in choice_data}
            for item in cleaned_data
        ]

        for item in ness_result:
            total_sum = sum(Decimal(value) for value in item.values())  
            item['총합'] = total_sum 

        for item in choice_result:
            total_sum = sum(Decimal(value) for value in item.values()) 
            item['총합'] = total_sum 

        data = {"ness_result":  ness_result,
                "choice_result": choice_result}

    return data


#교양 인성 계산
def liber_human_calculate(lecture_dict, user_liber_result):
    lectures_dict = [] #매개변수 담을 리스트
    user_liber_result = user_liber_result['human_result'] #[{'인간학': Decimal('4.0'), '트리니티아카데미': Decimal('2.0'), '총합': Decimal('6.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    normal_later = 0

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])
        print("DEF 교양 인성 과목 검수 하는 순서", needcheck)

        for liber_item in user_liber_result:
            if lecture_topic in liber_item:
                liber_credit = liber_item[lecture_topic]

                if lecture_credit < liber_credit:
                    missing_credit = liber_credit - lecture_credit
                    liber_item[lecture_topic] = missing_credit

                    delete_items.append(needcheck)

                    liber_item['총합'] -= lecture_credit

                elif lecture_credit > liber_credit:
                    del liber_item[lecture_topic]
                    missing_credit = liber_credit - lecture_credit
                    normal_later += abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                    delete_items.append(needcheck)

                    liber_item['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                elif lecture_credit == liber_credit:
                    del liber_item[lecture_topic]
                    liber_item['총합'] -= liber_credit

                    delete_items.append(needcheck)

            else:
                break

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

    for liber_item in user_liber_result:
        if '트리니티아카데미' in liber_item:
            for needcheck in lectures_dict[:]:
                lecture_topic = needcheck['주제']
                lecture_credit = Decimal(needcheck['학점'])

                if lecture_topic in ["정치와경제", "심리와건강", "정보와기술", "인간과문학", "역사와사회", "철학과예술", "자연과환경", "수리와과학", "언어와문화"]:
                    for liber_item in user_liber_result:
                        if "트리니티아카데미" in liber_item and liber_item["트리니티아카데미"] > lecture_credit:
                            liber_credit = liber_item["트리니티아카데미"]
                            missing_credit = liber_credit - lecture_credit
                            liber_item["트리니티아카데미"] = missing_credit
                            liber_item["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                        elif "트리니티아카데미" in liber_item and liber_item["트리니티아카데미"] == lecture_credit: 
                            del liber_item["트리니티아카데미"]
                            delete_items.append(needcheck)
                            liber_item["총합"] -= lecture_credit

                        elif "트리니티아카데미" in liber_item and liber_item["트리니티아카데미"] < lecture_credit: 
                            ness_credit = liber_item["트리니티아카데미"]
                            missing_credit = ness_credit - lecture_credit
                            normal_later += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del liber_item["트리니티아카데미"]
                            delete_items.append(needcheck)
                            
                            liber_item["총합"] -= lecture_credit    # 학점 기준 초과 시 반영
                        else:
                            break
        else:
            break


    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    print("DEF 교양 인성 일선 확인", normal_later)
    return lectures_dict, user_liber_result


#교양 융합 계산
def GE_fusion_calculate(lecture_dict, user_liber_result):
    lectures_dict = [] #매개변수 담을 리스트
    user_liber_result = user_liber_result['merge_result'] #[{'정보활용': Decimal('6.0'), '창의융합': Decimal('6.0'), '문제해결': Decimal('6.0'), '총합': Decimal('18.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    normal_later = 0

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])
        print("DEF 교양 융합 과목 검수 하는 순서", needcheck)

        GE_fusion_mapping_table = {
            '정치와경제' : '정보활용',
            '심리와건강' : '정보활용',
            '정보와기술' : '정보활용',
            '인간과문학' : '창의융합',
            '역사와사회' : '창의융합',
            '철학과예술' : '창의융합',
            '자연과환경' : '문제해결',
            '수리와과학' : '문제해결',
            '언어와문화' : '문제해결',
        }

        lecture_topic = GE_fusion_mapping_table.get(lecture_topic, lecture_topic)

        for liber_item in user_liber_result:
            if lecture_topic in liber_item:
                liber_credit = liber_item[lecture_topic]

                if lecture_credit < liber_credit:
                    missing_credit = liber_credit - lecture_credit
                    liber_item[lecture_topic] = missing_credit

                    delete_items.append(needcheck)

                    liber_item['총합'] -= lecture_credit

                elif lecture_credit > liber_credit:
                    print("DEF일선으로 빠지는 과목", needcheck)
                    del liber_item[lecture_topic]
                    missing_credit = liber_credit - lecture_credit
                    normal_later = abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                    delete_items.append(needcheck)

                    liber_item['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                elif lecture_credit == liber_credit:
                    del liber_item[lecture_topic]
                    liber_item['총합'] -= liber_credit

                    delete_items.append(needcheck)

            else:
                continue

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

    for liber_item in user_liber_result:
        if '융합비고' in liber_item:

            stack_info = []
            stack_fusion = []
            stack_problem = []

            for needcheck in lectures_dict[:]:
                lecture_topic = needcheck['주제']
                lecture_credit = Decimal(needcheck['학점'])

                if lecture_topic in ["정치와경제", "심리와건강", "정보와기술"]:

                    if len(stack_info) == 0:
                        stack_info.append(1)
                    else:
                        continue

                    for liber_item in user_liber_result:
                        if "융합비고" in liber_item and liber_item["융합비고"] > lecture_credit:
                            liber_credit = liber_item["융합비고"]
                            missing_credit = liber_credit - lecture_credit
                            liber_item["융합비고"] = missing_credit
                            liber_item["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                        elif "융합비고" in liber_item and liber_item["융합비고"] == lecture_credit: 
                            del liber_item["융합비고"]
                            delete_items.append(needcheck)
                            liber_item["총합"] -= lecture_credit

                        elif "융합비고" in liber_item and liber_item["융합비고"] < lecture_credit: 
                            liber_credit = liber_item["융합비고"]
                            missing_credit = liber_credit - lecture_credit
                            normal_later += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del liber_item["융합비고"]
                            delete_items.append(needcheck)
                            
                            liber_item["총합"] -= lecture_credit    # 학점 기준 초과 시 반영
                        else:
                            continue

                if lecture_topic in ["인간과문학", "역사와사회", "철학과예술"]:

                    if len(stack_fusion) == 0:
                        stack_fusion.append(1)
                    else:
                        continue

                    for liber_item in user_liber_result:
                        if "융합비고" in liber_item and liber_item["융합비고"] > lecture_credit:
                            liber_credit = liber_item["융합비고"]
                            missing_credit = liber_credit - lecture_credit
                            liber_item["융합비고"] = missing_credit
                            liber_item["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                        elif "융합비고" in liber_item and liber_item["융합비고"] == lecture_credit: 
                            del liber_item["융합비고"]
                            delete_items.append(needcheck)
                            liber_item["총합"] -= lecture_credit

                        elif "융합비고" in liber_item and liber_item["융합비고"] < lecture_credit: 
                            liber_credit = liber_item["융합비고"]
                            missing_credit = liber_credit - lecture_credit
                            normal_later += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del liber_item["융합비고"]
                            delete_items.append(needcheck)
                            
                            liber_item["총합"] -= lecture_credit    # 학점 기준 초과 시 반영
                        else:
                            continue

                if lecture_topic in ["자연과환경", "수리와과학", "언어와문화"]:

                    if len(stack_problem) == 0:
                        stack_problem.append(1)
                    else:
                        continue

                    for liber_item in user_liber_result:
                        if "융합비고" in liber_item and liber_item["융합비고"] > lecture_credit:
                            liber_credit = liber_item["융합비고"]
                            missing_credit = liber_credit - lecture_credit
                            liber_item["융합비고"] = missing_credit
                            liber_item["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                        elif "융합비고" in liber_item and liber_item["융합비고"] == lecture_credit: 
                            del liber_item["융합비고"]
                            delete_items.append(needcheck)
                            liber_item["총합"] -= lecture_credit

                        elif "융합비고" in liber_item and liber_item["융합비고"] < lecture_credit: 
                            liber_credit = liber_item["융합비고"]
                            missing_credit = liber_credit - lecture_credit
                            normal_later += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del liber_item["융합비고"]
                            delete_items.append(needcheck)
                            
                            liber_item["총합"] -= lecture_credit    # 학점 기준 초과 시 반영
                        else:
                            continue          

            for item in delete_items:
                if item in lectures_dict:
                    lectures_dict.remove(item)

        else:
            break

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    print("DEF교양 융합 일선 확인", normal_later)
    return lectures_dict, user_liber_result


#23년도 교양 기초 계산
def GE_basic_calculate(lecture_dict, user_liber_result, home_collage, year):
    lectures_dict = [] #매개변수 담을 리스트
    user_liber_result = user_liber_result['base_result'] #[{'논리적사고와글쓰기': Decimal('2.0'), '외국어': Decimal('4.0'), '자기관리': Decimal('6.0'), '총합': Decimal('12.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    normal_later = 0

    if year == '2023' and (home_collage == '1' or '2'):
        return
    elif year == '2023' and home_collage == '3':
        return
    elif year == '2024':
        return
    elif year == '2025':
        return
    return lectures_dict, user_liber_result