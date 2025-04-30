from .models import MyDoneLecture
from .models import liberRequire
from decimal import Decimal

#사용자 소속 대학 추출
def find_user_college(user_major):
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
def get_user_GE(user_id):
    student_id = user_id
    year = student_id[:4]

    mydone_lecture_list = MyDoneLecture.objects.filter(user_id=student_id, lecture_type__in=['교양', '교선', '교필'])
    lectures_dict = []
    done_GE = 0 #교양 총 학점 complete_liber_total_credit
    done_humanism_GE = 0 #교양 인성 총 학점 complete_general_human_credit
    done_basic_GE = 0 #교양 기초 총 학점 complete_general_base_credit
    done_fusion_GE = 0 #교양 융합 총 학점 complete_general_merge_credit
    done_essential_GE = 0 #complete_general_esse_credit
    done_choice_GE = 0 #complete_general_choice_credit

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
            done_GE += data['학점'] # 교양과목 총 이수 학점

        for data in lectures_dict[:]:
            if data['주제'] in {'VERUM캠프', '봉사활동', '인간학'}:
                done_humanism_GE += data['학점']    # 교양인성 총 이수 학점
            elif data['주제'] in {'소통', '논리적사고와글쓰기', '외국어', '디지털소통', '자기관리', '진로탐색', '창의성', '창업', '계열기초'}:
                done_basic_GE += data['학점']  # 교양기초 총 이수 학점
            elif data['주제'] in {'정치와경제', '심리와건강', '정보와기술', '인간과문학', '역사와사회', '철학과예술', '자연과환경', '수리와과학', '언어와문화'}:
                done_fusion_GE += data['학점'] #교양융합 총 이수 학점

        data = {"done_GE": done_GE,
                "done_humanism_GE": done_humanism_GE, 
                "done_basic_GE": done_basic_GE,
                "done_fusion_GE": done_fusion_GE}
    
    #트리니티 이전이라면
    else:

        for data in lectures_dict[:]:
            done_GE += data['학점'] # 교양과목 총 이수 학점

        for data in lectures_dict[:]:
            if data['주제'] in {'인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', 'MSC교과군', '철학적인간학', '신학적인간학'}:
                done_essential_GE += data['학점']    # 교양필수 총 이수 학점
            else:
                done_choice_GE += data['학점']  # 교양선택 총 이수 학점

        data = {
            "done_GE": done_GE,
            "done_essential_GE": done_essential_GE,
            "done_choice_GE": done_choice_GE
        }

    return lectures_dict, data


#사용자 교양요건 추출
def get_user_GE_standard(year, home_collage):
    filtered_data = liberRequire.objects.filter(연도=year).values()
    if(int(year) > 2022):

        #교양인성
        if(home_collage == '1'):
            humanism_GE_data = {'인간학'}
        #일반대학이고 23학번이라면 트리니티아카데미를 교양 요건으로 설정한다
        elif(home_collage == '3' and year == '2023'):
            humanism_GE_data = {'인간학', '트리니티아카데미'}
        else:
            humanism_GE_data = {'인간학', '봉사활동', 'VERUM캠프'}

        #교양기초
        basic_GE_data = {'소통', '논리적사고와글쓰기', '외국어', '자기관리', '진로탐색', '창의성', '창업', '계열기초', '디지털소통'}

        #교양융합
        if(year == '2025'):
            fusion_GE_data = {'정보활용', '창의융합', '문제해결', '융합비고'}
        else:
            fusion_GE_data = {'정보활용', '창의융합', '문제해결'}

        cleaned_data = [
            {key: value for key, value in item.items() if key not in ['liber_id', '연도'] and value != 0}
            for item in filtered_data
        ]
        humanism_GE_standard = [{key: value for key, value in item.items() if key in humanism_GE_data} for item in cleaned_data]
        basic_GE_standard = [{key: value for key, value in item.items() if key in basic_GE_data} for item in cleaned_data]
        fusion_GE_standard = [{key: value for key, value in item.items() if key in fusion_GE_data} for item in cleaned_data]

        humanism_GE_standard = [
            {key: value for key, value in item.items() if key in humanism_GE_data}
            for item in cleaned_data
        ]

        basic_GE_standard = [
            {key: value for key, value in item.items() if key in basic_GE_data}
            for item in cleaned_data
        ]

        fusion_GE_standard = [
            {key: value for key, value in item.items() if key in fusion_GE_data}
            for item in cleaned_data
        ]

        for item in humanism_GE_standard:
            total_sum = sum(Decimal(value) for value in item.values())  
            item['총합'] = total_sum 

        for item in basic_GE_standard:
            total_sum = sum(Decimal(value) for value in item.values()) 
            item['총합'] = total_sum 

        for item in fusion_GE_standard:
            total_sum = sum(Decimal(value) for value in item.values()) 
            item['총합'] = total_sum 

        data = {"humanism_GE_standard": humanism_GE_standard,
                "basic_GE_standard": basic_GE_standard,
                "fusion_GE_standard": fusion_GE_standard}

    else:
        # 교양필수 주제 (18 ~ 22년도 : 트리니티 이전)
        essential_GE_data = {'인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', 'MSC교과군', '철학적인간학', '신학적인간학', 'VERUM인성'}
        
        # 교양선택 주제 (18 ~ 22년도 : 트리니티 이전)
        choice_GE_data = {'고전탐구', '사유와지혜', '가치와실천', '상상력과표현', '인문융합', '균형1', '균형2', '균형3', '균형4', '계열기초'}
        
        cleaned_data = [
            {key: value for key, value in item.items() if key not in ['liber_id', '연도'] and value != 0}
            for item in filtered_data
        ]

        essential_GE_standard = [{key: value for key, value in item.items() if key in essential_GE_data} for item in cleaned_data]
        chocie_GE_standard = [{key: value for key, value in item.items() if key in choice_GE_data} for item in cleaned_data]
        
        essential_GE_standard = [
            {key: value for key, value in item.items() if key in essential_GE_data}
            for item in cleaned_data
        ]

        chocie_GE_standard = [
            {key: value for key, value in item.items() if key in choice_GE_data}
            for item in cleaned_data
        ]

        for item in essential_GE_standard:
            total_sum = sum(Decimal(value) for value in item.values())  
            item['총합'] = total_sum 

        for item in chocie_GE_standard:
            total_sum = sum(Decimal(value) for value in item.values()) 
            item['총합'] = total_sum 

        data = {"essential_GE_standard":  essential_GE_standard,
                "chocie_GE_standard": chocie_GE_standard}

    print("교양요건 추출", data)
    return data


#교양 인성 계산
def GE_humanism_calculate(lecture_dict, user_GE_standard):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['humanism_GE_standard'] #[{'인간학': Decimal('4.0'), '트리니티아카데미': Decimal('2.0'), '총합': Decimal('6.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = 0


    #교양 인성 인간학, 봉사활동, VERUM캠프 계산(주제가 DB의 교양요건과 동일한 경우)
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])
        print("DEF 교양 인성 과목 검수 하는 순서", needcheck)

        for GE_standard in user_GE_standard:
            if lecture_topic in GE_standard:
                GE_credit = GE_standard[lecture_topic]

                if lecture_credit < GE_credit:
                    missing_credit = GE_credit - lecture_credit
                    GE_standard[lecture_topic] = missing_credit

                    delete_items.append(needcheck)

                    GE_standard['총합'] -= lecture_credit

                elif lecture_credit > GE_credit:
                    del GE_standard[lecture_topic]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)

                    delete_items.append(needcheck)

                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit)) 

                elif lecture_credit == GE_credit:
                    del GE_standard[lecture_topic]
                    GE_standard['총합'] -= GE_credit

                    delete_items.append(needcheck)

            else:
                break

    #삭제명단에 오른 과목 데이터 삭제
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #23년도 트리니티아카데미 대체과목 계산 로직 (트리니티아카데미가 있을 경우에만)
    for GE_standard in user_GE_standard:
        if '트리니티아카데미' in GE_standard:
            for needcheck in lectures_dict[:]:
                lecture_topic = needcheck['주제']
                lecture_credit = Decimal(needcheck['학점'])

                #대체과목 영역이 사용자 교양 들은 과목에 존재한다면 트리니티아카데미를 계산한다
                if lecture_topic in ["정치와경제", "심리와건강", "정보와기술", "인간과문학", "역사와사회", "철학과예술", "자연과환경", "수리와과학", "언어와문화"]:
                    for GE_standard in user_GE_standard:
                        if "트리니티아카데미" in GE_standard and GE_standard["트리니티아카데미"] > lecture_credit:
                            GE_credit = GE_standard["트리니티아카데미"]
                            missing_credit = GE_credit - lecture_credit
                            GE_standard["트리니티아카데미"] = missing_credit
                            GE_standard["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                        elif "트리니티아카데미" in GE_standard and GE_standard["트리니티아카데미"] == lecture_credit: 
                            del GE_standard["트리니티아카데미"]
                            delete_items.append(needcheck)
                            GE_standard["총합"] -= lecture_credit

                        elif "트리니티아카데미" in GE_standard and GE_standard["트리니티아카데미"] < lecture_credit: 
                            GE_credit = GE_standard["트리니티아카데미"]
                            missing_credit = GE_credit - lecture_credit
                            rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del GE_standard["트리니티아카데미"]
                            delete_items.append(needcheck)
                            
                            GE_standard["총합"] -= lecture_credit    # 학점 기준 초과 시 반영
                        else:
                            break
        else:
            break


    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    print("DEF 교양 인성 일선 확인", rest_total)
    return lectures_dict, user_GE_standard, rest_total


#교양 융합 계산
def GE_fusion_calculate(lecture_dict, user_GE_standard, rest_total):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['fusion_GE_standard'] #[{'정보활용': Decimal('6.0'), '창의융합': Decimal('6.0'), '문제해결': Decimal('6.0'), '총합': Decimal('18.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = rest_total

    #택1, 택2 과정에서 영역 중복 수강 방지를 위해 stack 생성
    stack_economy = []
    stack_health = []
    stack_tech = []
    stack_lit = []
    stack_society = []
    stack_art = []
    stack_env = []
    stack_science = []
    stack_culture = []

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        #각 영역이 사용자가 들은 과목에 들어가 있다면 해당 영역의 교양요건 계산 (정보활용)
        if lecture_topic in ["정치와경제"]:
            print("DEF 교양 융합 정보활용-정치와경제", needcheck)

            #해당 주제 stack에 값이 들어갔는지를 확인
            if len(stack_economy) == 0:
                stack_economy.append(1)
            #한 개 이상들어갔다면 아래 for문 무시
            else:
                continue

            for GE_standard in user_GE_standard:
                if "정보활용" in GE_standard and GE_standard["정보활용"] > lecture_credit:
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["정보활용"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "정보활용" in GE_standard and GE_standard["정보활용"] == lecture_credit: 
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "정보활용" in GE_standard and GE_standard["정보활용"] < lecture_credit: 
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) 
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= lecture_credit 
                else:
                    continue

        if lecture_topic in ["심리와건강"]:
            print("DEF 교양 융합 정보활용-심리와건강", needcheck)

            if len(stack_health) == 0:
                stack_health.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "정보활용" in GE_standard and GE_standard["정보활용"] > lecture_credit:
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["정보활용"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "정보활용" in GE_standard and GE_standard["정보활용"] == lecture_credit: 
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "정보활용" in GE_standard and GE_standard["정보활용"] < lecture_credit: 
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) 
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= lecture_credit    
                else:
                    continue

        if lecture_topic in ["정보와기술"]:
            print("DEF 교양 융합 정보활용-정보와기술", needcheck)

            if len(stack_tech) == 0:
                stack_tech.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "정보활용" in GE_standard and GE_standard["정보활용"] > lecture_credit:
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["정보활용"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "정보활용" in GE_standard and GE_standard["정보활용"] == lecture_credit: 
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "정보활용" in GE_standard and GE_standard["정보활용"] < lecture_credit: 
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= lecture_credit    
                else:
                    continue

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #각 영역이 사용자가 들은 과목에 들어가 있다면 해당 영역의 교양요건 계산 (창의융합)
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["인간과문학"]:
            print("DEF 교양 융합 정보활용", needcheck)

            if len(stack_lit) == 0:
                stack_lit.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "창의융합" in GE_standard and GE_standard["창의융합"] > lecture_credit:
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["창의융합"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "창의융합" in GE_standard and GE_standard["창의융합"] == lecture_credit: 
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "창의융합" in GE_standard and GE_standard["창의융합"] < lecture_credit: 
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) 
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= lecture_credit   
                else:
                    continue

        if lecture_topic in ["역사와사회"]:
            print("DEF 교양 융합 정보활용", needcheck)

            if len(stack_society) == 0:
                stack_society.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "창의융합" in GE_standard and GE_standard["창의융합"] > lecture_credit:
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["창의융합"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "창의융합" in GE_standard and GE_standard["창의융합"] == lecture_credit: 
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "창의융합" in GE_standard and GE_standard["창의융합"] < lecture_credit: 
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) 
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= lecture_credit  
                else:
                    continue

        if lecture_topic in ["철학과예술"]:
            print("DEF 교양 융합 정보활용", needcheck)

            if len(stack_art) == 0:
                stack_art.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "창의융합" in GE_standard and GE_standard["창의융합"] > lecture_credit:
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["창의융합"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "창의융합" in GE_standard and GE_standard["창의융합"] == lecture_credit: 
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "창의융합" in GE_standard and GE_standard["창의융합"] < lecture_credit: 
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= lecture_credit  
                else:
                    continue

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #각 영역이 사용자가 들은 과목에 들어가 있다면 해당 영역의 교양요건 계산 (문제해결)
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["자연과환경"]:
            print("DEF 교양 융합 정보활용", needcheck)

            if len(stack_env) == 0:
                stack_env.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "문제해결" in GE_standard and GE_standard["문제해결"] > lecture_credit:
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["문제해결"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "문제해결" in GE_standard and GE_standard["문제해결"] == lecture_credit: 
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "문제해결" in GE_standard and GE_standard["문제해결"] < lecture_credit: 
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= lecture_credit
                else:
                    continue

        if lecture_topic in ["수리와과학"]:
            print("DEF 교양 융합 정보활용", needcheck)

            if len(stack_science) == 0:
                stack_science.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "문제해결" in GE_standard and GE_standard["문제해결"] > lecture_credit:
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["문제해결"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "문제해결" in GE_standard and GE_standard["문제해결"] == lecture_credit: 
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "문제해결" in GE_standard and GE_standard["문제해결"] < lecture_credit: 
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= lecture_credit   
                else:
                    continue

        if lecture_topic in ["언어와문화"]:
            print("DEF 교양 융합 정보활용", needcheck)

            if len(stack_culture) == 0:
                stack_culture.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "문제해결" in GE_standard and GE_standard["문제해결"] > lecture_credit:
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["문제해결"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "문제해결" in GE_standard and GE_standard["문제해결"] == lecture_credit: 
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "문제해결" in GE_standard and GE_standard["문제해결"] < lecture_credit: 
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= lecture_credit    # 학점 기준 초과 시 반영
                else:
                    continue

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #각 영역이 사용자가 들은 과목에 들어가 있다면 해당 영역의 교양요건 계산 (융합비고) => 교양 요건에 융합비고가 있는 경우에만 작동
    for GE_standard in user_GE_standard:
        if '융합비고' in GE_standard:
            print("융합비고 들어왔는지")

            stack_info = []
            stack_fusion = []
            stack_problem = []

            for needcheck in lectures_dict[:]:
                lecture_topic = needcheck['주제']
                lecture_credit = Decimal(needcheck['학점'])

                if lecture_topic in ["정치와경제", "심리와건강", "정보와기술"]:

                    if len(stack_info) == 0:
                        stack_info.append(1)
                        print("DEF 교양 융합 융합비고", needcheck)
                    else:
                        continue

                    for GE_standard in user_GE_standard:
                        if "융합비고" in GE_standard and GE_standard["융합비고"] > lecture_credit:
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            GE_standard["융합비고"] = missing_credit
                            GE_standard["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] == lecture_credit: 
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            GE_standard["총합"] -= lecture_credit

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] < lecture_credit: 
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            
                            GE_standard["총합"] -= lecture_credit    # 학점 기준 초과 시 반영
                        else:
                            continue

                if lecture_topic in ["인간과문학", "역사와사회", "철학과예술"]:

                    if len(stack_fusion) == 0:
                        stack_fusion.append(1)
                    else:
                        continue

                    for GE_standard in user_GE_standard:
                        if "융합비고" in GE_standard and GE_standard["융합비고"] > lecture_credit:
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            GE_standard["융합비고"] = missing_credit
                            GE_standard["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] == lecture_credit: 
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            GE_standard["총합"] -= lecture_credit

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] < lecture_credit: 
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            
                            GE_standard["총합"] -= lecture_credit    # 학점 기준 초과 시 반영
                        else:
                            continue

                if lecture_topic in ["자연과환경", "수리와과학", "언어와문화"]:

                    if len(stack_problem) == 0:
                        stack_problem.append(1)
                    else:
                        continue

                    for GE_standard in user_GE_standard:
                        if "융합비고" in GE_standard and GE_standard["융합비고"] > lecture_credit:
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            GE_standard["융합비고"] = missing_credit
                            GE_standard["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] == lecture_credit: 
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            GE_standard["총합"] -= lecture_credit

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] < lecture_credit: 
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            
                            GE_standard["총합"] -= lecture_credit    # 학점 기준 초과 시 반영
                        else:
                            continue          

            for item in delete_items:
                if item in lectures_dict:
                    lectures_dict.remove(item)
            delete_items = []

        else:
            break

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []
    print("DEF교양 융합 일선 확인", rest_total)
    return lectures_dict, user_GE_standard, rest_total


#23년도 교양 기초 계산
def GE_basic_calculate_2023(lecture_dict, user_GE_standard, home_collage, rest_total):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['basic_GE_standard'] #[{'논리적사고와글쓰기': Decimal('2.0'), '외국어': Decimal('4.0'), '자기관리': Decimal('6.0'), '총합': Decimal('12.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = rest_total

    #계열기초
    stack_major_base = []
    #창의성
    stack_creative = []
    #창업
    stack_startup = []
    #진로탐색
    stack_search = []

    #일반대학의 경우
    if (home_collage == '3'):
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            for GE_standard in user_GE_standard:
                if lecture_topic in GE_standard:
                    GE_credit = GE_standard[lecture_topic]

                    if lecture_credit < GE_credit:
                        missing_credit = GE_credit - lecture_credit
                        GE_standard[lecture_topic] = missing_credit

                        delete_items.append(needcheck)

                        GE_standard['총합'] -= lecture_credit

                    elif lecture_credit > GE_credit:
                        del GE_standard[lecture_topic]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                        delete_items.append(needcheck)

                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    elif lecture_credit == GE_credit:
                        del GE_standard[lecture_topic]
                        GE_standard['총합'] -= GE_credit

                        delete_items.append(needcheck)

                else:
                    break

        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []

        #창의 계산 (택1을 위해 순차적으로 창의성 먼저 계산)
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            if lecture_topic in ["창의성"]:

                if len(stack_creative) == 0:
                    stack_creative.append(1)
                else:
                    continue

                for GE_standard in user_GE_standard:
                    if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                    else:
                        break

        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []
    
        #창업 계산 (택1을 위해 순차적으로 창업 먼저 계산)
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            if lecture_topic in ["창업"]:

                if len(stack_startup) == 0:
                    stack_startup.append(1)
                else:
                    continue

                for GE_standard in user_GE_standard:
                    if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                    else:
                        break

        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []

        #진로탐색 계산 (택1을 위해 순차적으로 진로탐색 먼저 계산)
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            if lecture_topic in ["진로탐색"]:

                if len(stack_search) == 0:
                    stack_search.append(1)
                elif len(stack_search) == 1:
                    stack_search.append(1)
                elif len(stack_search) == 2:
                    stack_search.append(1)
                else:
                    continue

                for GE_standard in user_GE_standard:
                    if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                    else:
                        break

        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []

    #의과, 헬스케어, 사범, 휴먼서비스의 경우
    else:
        #논리적사고와글쓰기, 외국어 계산(주제와 교양요건이 동일한 경우)
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            for GE_standard in user_GE_standard:
                if lecture_topic in GE_standard:
                    GE_credit = GE_standard[lecture_topic]

                    if lecture_credit < GE_credit:
                        missing_credit = GE_credit - lecture_credit
                        GE_standard[lecture_topic] = missing_credit

                        delete_items.append(needcheck)

                        GE_standard['총합'] -= lecture_credit

                    elif lecture_credit > GE_credit:
                        del GE_standard[lecture_topic]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                        delete_items.append(needcheck)

                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    elif lecture_credit == GE_credit:
                        del GE_standard[lecture_topic]
                        GE_standard['총합'] -= GE_credit

                        delete_items.append(needcheck)

                else:
                    break

        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []

        #계열기초 계산(택1을 위해 순차적으로 계열기초 먼저 계산)
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            if lecture_topic in ["계열기초"]:

                if len(stack_major_base) == 0:
                    stack_major_base.append(1)
                elif len(stack_major_base) == 1:
                    stack_major_base.append(1)
                else:
                    continue

                for GE_standard in user_GE_standard:
                    if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                    else:
                        break

        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []

        #창의성 계산(택1을 위해 순차적으로 창의성 먼저 계산)
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            if lecture_topic in ["창의성"]:

                if len(stack_creative) == 0:
                    stack_creative.append(1)
                else:
                    continue

                for GE_standard in user_GE_standard:
                    if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                    else:
                        break
                    
        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []

        #창업 계산(택1을 위해 순차적으로 창업 먼저 계산)
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            if lecture_topic in ["창업"]:

                if len(stack_startup) == 0:
                    stack_startup.append(1)
                else:
                    continue

                for GE_standard in user_GE_standard:
                    if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                    else:
                        break
                    
        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []

        #진로탐색 계산 (택1을 위해 순차적으로 진로탐색 먼저 계산)
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            if lecture_topic in ["진로탐색"]:

                if len(stack_search) == 0:
                    stack_search.append(1)
                else:
                    continue

                for GE_standard in user_GE_standard:
                    if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                    else:
                        break
                    
        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []

    print("일선 확인", rest_total)
    return lectures_dict, user_GE_standard, rest_total

#24, 25년도 교양 기초 계산
def GE_basic_calculate_2025(lecture_dict, user_GE_standard, rest_total):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['basic_GE_standard'] #[{'논리적사고와글쓰기': Decimal('2.0'), '외국어': Decimal('4.0'), '자기관리': Decimal('6.0'), '총합': Decimal('12.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = rest_total

    #논리적사고와글쓰기
    stack_write = []
    #계열기초
    stack_major_base = []
    #창의성
    stack_creative = []
    #창업
    stack_startup = []
    #진로탐색
    stack_search = []

    #디지털소통 계산(주제와 교양 요건이 동일한 경우)
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        for GE_standard in user_GE_standard:
            if lecture_topic in GE_standard:
                GE_credit = GE_standard[lecture_topic]

                if lecture_credit < GE_credit:
                    missing_credit = GE_credit - lecture_credit
                    GE_standard[lecture_topic] = missing_credit

                    delete_items.append(needcheck)

                    GE_standard['총합'] -= lecture_credit

                elif lecture_credit > GE_credit:
                    del GE_standard[lecture_topic]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                    delete_items.append(needcheck)

                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                elif lecture_credit == GE_credit:
                    del GE_standard[lecture_topic]
                    GE_standard['총합'] -= GE_credit

                    delete_items.append(needcheck)

            else:
                break

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #논사글 계산
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["논리적사고와글쓰기"]:

            if len(stack_write) == 0:
                stack_write.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "소통" in GE_standard and GE_standard["소통"] > lecture_credit:
                    GE_credit = GE_standard["소통"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["소통"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "소통" in GE_standard and GE_standard["소통"] == lecture_credit: 
                    del GE_standard["소통"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "소통" in GE_standard and GE_standard["소통"] < lecture_credit: 
                    GE_credit = GE_standard["소통"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["소통"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                else:
                    break
                
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #외국어 계산
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["외국어"]:

            for GE_standard in user_GE_standard:
                if "소통" in GE_standard and GE_standard["소통"] > lecture_credit:
                    GE_credit = GE_standard["소통"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["소통"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "소통" in GE_standard and GE_standard["소통"] == lecture_credit: 
                    del GE_standard["소통"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "소통" in GE_standard and GE_standard["소통"] < lecture_credit: 
                    GE_credit = GE_standard["소통"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["소통"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                else:
                    break
                
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #계열기초 계산
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["계열기초"]:

            if len(stack_major_base) == 0:
                stack_major_base.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["자기관리"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                else:
                    break
                
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #창의 계산
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["창의성"]:

            if len(stack_creative) == 0:
                stack_creative.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["자기관리"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                else:
                    break
                
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #창업 계산
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["창업"]:

            if len(stack_startup) == 0:
                stack_startup.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["자기관리"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                else:
                    break
                
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #진로탐색 계산
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["진로탐색"]:

            if len(stack_search) == 0:
                stack_search.append(1)
            elif len(stack_search) == 1:
                stack_search.append(1)
            else:
                continue

            for GE_standard in user_GE_standard:
                if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["자기관리"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    
                    GE_standard["총합"] -= GE_credit    # 학점 기준 초과 시 반영
                else:
                    break
                
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    print("일선 계산확인", rest_total)
    return lectures_dict, user_GE_standard, rest_total