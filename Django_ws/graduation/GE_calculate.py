from django.db import IntegrityError
from decimal import Decimal
from user.models import User
from .models import MyDoneLecture
from .models import GEStandard

# 소속 대학 분류
def find_user_college(user_major):
    medical_college = ['030501*', '030503*']  # 의예과(1~2학년) / 의학과(3~6학년)
    health_care_college = ['032801*', '032802*']  # 임상병리학과 / 치위생학과
    human_service_college = ['032703*', '032705*', '032708*', '032709*', '032710*', '032702*']  # 산림치유, 언어재활, 중독재활/중독재활상담/복지상담, 통합치유/스마트통합치유, 해양치유레저, 치매전문재활
    education_college = ['030701*', '030704*', '030710*', '030709*', '030702*', '030705*', '030707*']  # 국어교육과, 수학교육과, 역사교육과, 영어교육과, 지리교육과, 체육교육과, 컴퓨터교육과

    major = user_major['major']

    if major in human_service_college:
        user_college = 'human_service'

    elif major in (medical_college + health_care_college + education_college):
        user_college = 'regular'

    else:
        user_college = 'trinity'

    return user_college

#사용자 교양 이수학점 계산
def get_user_GE(user_id):
    student_id = user_id
    year = int(student_id[:4])

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
    if (year > 2022):

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
def get_user_GE_standard(year, user_college):
    filtered_data = GEStandard.objects.filter(연도=year).values()
    if(int(year) > 2022):

        #교양인성
        if(user_college == 'human_service'):
            humanism_GE_data = {'인간학'}
        #일반대학이고 23학번이라면 트리니티아카데미를 교양 요건으로 설정한다
        elif(user_college == 'trinity' and year == '2023'):
            humanism_GE_data = {'인간학', '트리니티아카데미'}
        else:
            humanism_GE_data = {'인간학', '봉사활동', 'VERUM캠프'}

        basic_GE_data = {'소통', '논리적사고와글쓰기', '외국어', '자기관리', '진로탐색', '창의성', '창업', '계열기초', '디지털소통'}

        if (user_college == 'human_service' and year == '2023'):
            filtered_data = GEStandard.objects.filter(연도='2023B').values()
            #교양기초
            basic_GE_data = {'소통', '논리적사고와글쓰기', '외국어', '자기관리', '진로탐색', '창의성', '창업', '계열기초', '디지털소통'}
        elif (user_college == 'regular' and year == '2023'):
            filtered_data = GEStandard.objects.filter(연도='2023B').values()
            #교양기초
            basic_GE_data = {'소통', '논리적사고와글쓰기', '외국어', '자기관리', '진로탐색', '창의성', '창업', '계열기초', '디지털소통'}

        #교양융합
        if(year == '2025'):
            fusion_GE_data = {'정보활용', '창의융합', '문제해결', '융합비고'}
        else:
            fusion_GE_data = {'정보활용', '창의융합', '문제해결'}

        cleaned_data = [
            {key: value for key, value in item.items() if key not in ['GEStandard_id', '연도'] and value != 0}
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
            {key: value for key, value in item.items() if key not in ['GEStandard_id', '연도'] and value != 0}
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

#사용자 교양 부족 영역 계산
def GE_all_calculate(user_id):
    student_id = user_id
    year = student_id[:4]   # 학번 전처리 (년도 추출)  ex) 2020xxxx > 2020
    user_college = 0

    #교양 이수학점 계산 및 교양 과목 추출
    lecture_dict, liber_credit = get_user_GE(user_id)
    lectures_dict = []
    lectures_dict = lecture_dict
    done_GE = liber_credit['done_GE']
    done_essential_GE = liber_credit['done_essential_GE']
    done_choice_GE = liber_credit['done_choice_GE']

    #교양 필수, 선택 영역 추출
    user_GE_standard = get_user_GE_standard(year, user_college)
    essential_GE_standard = user_GE_standard['essential_GE_standard']
    chocie_GE_standard = user_GE_standard['chocie_GE_standard']
    
    delete_items = []
    rest = 0

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        for essential_stanadard in essential_GE_standard:
            if lecture_topic in essential_stanadard:
                essential_credit = essential_stanadard[lecture_topic]

                if lecture_credit < essential_credit:
                    missing_credit = essential_credit - lecture_credit
                    essential_stanadard[lecture_topic] = missing_credit

                    delete_items.append(needcheck)

                    essential_stanadard['총합'] -= lecture_credit

                elif lecture_credit > essential_credit:
                    del essential_stanadard[lecture_topic]
                    missing_credit = essential_credit - lecture_credit
                    rest += abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                    delete_items.append(needcheck)

                    essential_stanadard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                elif lecture_credit == essential_credit:
                    del essential_stanadard[lecture_topic]
                    essential_stanadard['총합'] -= essential_credit

                    delete_items.append(needcheck)

            else:
                break
    
    # print('수강 인정 교필 과목 (삭제) : ')
    # pprint.pprint(delete_items, width=80, sort_dicts=False)

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)


    ######################################################## 교선 영역 계산 ########################################################

    ###### '고전탐구', '사유와지혜', '가치와실천', '상상력과표현', '인문융합', '균형1', '균형2', '균형3', '균형4', '계열기초' ######

    ####################################################### 실질적 확인 영역 #######################################################
    ######################################## '균형1', '균형2', '균형3', '균형4', '계열기초' ########################################

    delete_items = []

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        for choice_standard in chocie_GE_standard:
            if lecture_topic in choice_standard:
                choice_credit = choice_standard[lecture_topic]

                if lecture_credit < choice_credit:
                    missing_credit = choice_credit - lecture_credit
                    choice_standard[lecture_topic] = missing_credit


                    delete_items.append(needcheck)

                    choice_standard['총합'] -= lecture_credit

                elif lecture_credit > choice_credit:
                    del choice_standard[lecture_topic]
                    missing_credit = lecture_credit - choice_credit
                    rest += missing_credit # 초과 학점 일반선택 학점 추가

                    delete_items.append(needcheck)
                    choice_standard['총합'] -= choice_credit   # 학점 기준 초과 시 반영

                elif lecture_credit == choice_credit:
                    del choice_standard[lecture_topic]
                    choice_standard['총합'] -= choice_credit

                    delete_items.append(needcheck)

            else:
                break
    

    # print('수강 인정 교선 과목 (삭제) : ')
    # pprint.pprint(delete_items, width=80, sort_dicts=False)

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

    ######################################################## 교필 대체과목 영역 계산 ########################################################

    delete_items = []

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["정보와기술", "자연과환경", "수리와과학"]:
            for essential_stanadard in essential_GE_standard:
                if "MSC교과군" in essential_stanadard and essential_stanadard["MSC교과군"] > lecture_credit:
                    essential_credit = essential_stanadard["MSC교과군"]
                    missing_credit = essential_credit - lecture_credit
                    essential_stanadard["MSC교과군"] = missing_credit
                    essential_stanadard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "MSC교과군" in essential_stanadard and essential_stanadard["MSC교과군"] == lecture_credit: 
                    del essential_stanadard["MSC교과군"]
                    delete_items.append(needcheck)
                    essential_stanadard["총합"] -= lecture_credit

                elif "MSC교과군" in essential_stanadard and essential_stanadard["MSC교과군"] < lecture_credit: 
                    essential_credit = essential_stanadard["MSC교과군"]
                    missing_credit = essential_credit - lecture_credit
                    rest += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del essential_stanadard["MSC교과군"]
                    delete_items.append(needcheck)
                    
                    essential_stanadard["총합"] -= choice_credit    # 학점 기준 초과 시 반영
                else:
                    break

    # print('수강 인정 교선 과목 (삭제) : ')
    # pprint.pprint(delete_items, width=80, sort_dicts=False)

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

    ######################################################## 교필 대체과목 영역 계산(18 ~ 19) ########################################################

    delete_items = []

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["정보와기술"]:
            for essential_stanadard in essential_GE_standard:
                if "창의적사고와코딩" in essential_stanadard and essential_stanadard["창의적사고와코딩"] > lecture_credit:
                    essential_credit = essential_stanadard["창의적사고와코딩"]
                    missing_credit = essential_credit - lecture_credit
                    essential_stanadard["창의적사고와코딩"] = missing_credit
                    essential_stanadard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "창의적사고와코딩" in essential_stanadard and essential_stanadard["창의적사고와코딩"] == lecture_credit: 
                    del essential_stanadard["창의적사고와코딩"]
                    delete_items.append(needcheck)
                    essential_stanadard["총합"] -= lecture_credit

                elif "창의적사고와코딩" in essential_stanadard and essential_stanadard["창의적사고와코딩"] < lecture_credit: 
                    essential_credit = essential_stanadard["창의적사고와코딩"]
                    missing_credit = essential_credit - lecture_credit
                    rest += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del essential_stanadard["창의적사고와코딩"]
                    delete_items.append(needcheck)
                    
                    essential_stanadard["총합"] -= choice_credit    # 학점 기준 초과 시 반영
                else:
                    break

    # print('수강 인정 교선 과목 (삭제) : ')
    # pprint.pprint(delete_items, width=80, sort_dicts=False)

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

    ############################################## 교선 균형 1, 2, 3, 4 대체과목 반영 ##############################################

    delete_items = []


    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic == "언어와문화":

            for choice_standard in chocie_GE_standard:
                if "균형1" in choice_standard: 
                    choice_credit = choice_standard["균형1"]

                    if lecture_credit == choice_credit:
                        del choice_standard["균형1"]
                        choice_standard["총합"] -= choice_credit

                        delete_items.append(needcheck) 
                    break
        
        if lecture_topic == "정치와경제":

            for choice_standard in chocie_GE_standard:
                if "균형2" in choice_standard: 
                    choice_credit = choice_standard["균형2"]

                    if lecture_credit == choice_credit:
                        del choice_standard["균형2"]
                        choice_standard["총합"] -= choice_credit

                        delete_items.append(needcheck) 
                    
                    elif lecture_credit > choice_credit:
                        missing_credit = lecture_credit - choice_credit 
                        rest += missing_credit
                        del choice_standard["균형2"]

                        delete_items.append(needcheck)

                        choice_standard["총합"] -= choice_credit
                    break

        if lecture_topic == "정보와기술":

            for choice_standard in chocie_GE_standard:
                if "균형3" in choice_standard: 
                    choice_credit = choice_standard["균형3"]

                    if lecture_credit == choice_credit:
                        del choice_standard["균형3"]
                        choice_standard["총합"] -= choice_credit

                        delete_items.append(needcheck)


                    elif lecture_credit > choice_credit:
                        missing_credit = lecture_credit - choice_credit 
                        rest += missing_credit
                        del choice_standard["균형3"]

                        delete_items.append(needcheck)

                        choice_standard["총합"] -= choice_credit
                    break

        if lecture_topic == "심리와건강":

            for choice_standard in chocie_GE_standard:
                if "균형4" in choice_standard: 
                    choice_credit = choice_standard["균형4"]

                    if lecture_credit == choice_credit:
                        del choice_standard["균형4"]
                        choice_standard["총합"] -= choice_credit

                        delete_items.append(needcheck) 
                    break

    # print('수강 인정 교선 과목 (삭제) : ')
    # pprint.pprint(delete_items, width=80, sort_dicts=False)

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

    
    ############################### 고전탐구 / 사유와지혜 / 가치와실천 / 상상력과표현 / 인문융합 ##############################

    delete_items = []


    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["인간과문학", "역사와사회", "철학과예술"]:
            for choice_standard in chocie_GE_standard:
                if "고전탐구" in choice_standard and choice_standard["고전탐구"] == lecture_credit:
                    del choice_standard["고전탐구"] 
                    choice_standard["총합"] -= lecture_credit  
                    if needcheck not in delete_items:
                        delete_items.append(needcheck)
                    break
                
                if "사유와지혜" in choice_standard and choice_standard["사유와지혜"] == lecture_credit:
                    del choice_standard["사유와지혜"] 
                    choice_standard["총합"] -= lecture_credit
                    if needcheck not in delete_items:
                        delete_items.append(needcheck)
                    break

                if "가치와실천" in choice_standard and choice_standard["가치와실천"] == lecture_credit:
                    del choice_standard["가치와실천"] 
                    choice_standard["총합"] -= lecture_credit
                    if needcheck not in delete_items:
                        delete_items.append(needcheck)
                    break

                if "상상력과표현" in choice_standard and choice_standard["상상력과표현"] == lecture_credit:
                    del choice_standard["상상력과표현"]
                    choice_standard["총합"] -= lecture_credit
                    if needcheck not in delete_items:
                        delete_items.append(needcheck)
                    break

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

    
    ############################################## 단과대학별 과목 (19학번) 반영 ##############################################
    ################################################ 인문융합 과목 (20 ~) 반영 ################################################

    delete_items = []


    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic in ["인간과문학", "역사와사회", "철학과예술"]:
            for choice_standard in chocie_GE_standard:
                if "인문융합" in choice_standard and choice_standard["인문융합"] > lecture_credit:
                    choice_credit = choice_standard["인문융합"]
                    missing_credit = choice_credit - lecture_credit
                    choice_standard["인문융합"] = missing_credit
                    choice_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "인문융합" in choice_standard and choice_standard["인문융합"] == lecture_credit: 
                    del choice_standard["인문융합"]
                    delete_items.append(needcheck)
                    choice_standard["총합"] -= lecture_credit  
                break


    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)


    ######################################### 균형 1, 2, 3, 4 영역 대체과목 반영 (교집합) #########################################

    delete_items = []

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        if lecture_topic == "인간과문학":

            for choice_standard in chocie_GE_standard:
                if "균형1" in choice_standard: 
                    choice_credit = choice_standard["균형1"]

                    if lecture_credit == choice_credit:
                        del choice_standard["균형1"]
                        choice_standard["총합"] -= lecture_credit

                        delete_items.append(needcheck) 
                    break
        
        if lecture_topic == "역사와사회":

            for choice_standard in chocie_GE_standard:
                if "균형2" in choice_standard: 
                    choice_credit = choice_standard["균형2"]

                    if lecture_credit == choice_credit:
                        del choice_standard["균형2"]
                        choice_standard["총합"] -= lecture_credit

                        delete_items.append(needcheck) 
                    break

        if lecture_topic == "자연과환경":

            for choice_standard in chocie_GE_standard:
                if "균형3" in choice_standard: 
                    choice_credit = choice_standard["균형3"]

                    if lecture_credit == choice_credit:
                        del choice_standard["균형3"]
                        choice_standard["총합"] -= lecture_credit

                        delete_items.append(needcheck) 
                    elif lecture_credit > choice_credit:
                        missing_credit = lecture_credit - choice_credit
                        rest += missing_credit
                        del choice_standard["균형3"]

                        choice_standard["총합"] -= choice_credit
                    break


        if lecture_topic == "수리와과학":

            for choice_standard in chocie_GE_standard:
                if "균형3" in choice_standard: 
                    choice_credit = choice_standard["균형3"]

                    if lecture_credit == choice_credit:
                        del choice_standard["균형3"]
                        choice_standard["총합"] -= lecture_credit

                        delete_items.append(needcheck) 
                    elif lecture_credit > choice_credit:
                        missing_credit = lecture_credit - choice_credit
                        rest += missing_credit
                        del choice_standard["균형3"]

                        choice_standard["총합"] -= choice_credit
                    break


        if lecture_topic == "철학과예술":

            for choice_standard in chocie_GE_standard:
                if "균형4" in choice_standard: 
                    choice_credit = choice_standard["균형4"]

                    if lecture_credit == choice_credit:
                        del choice_standard["균형4"]
                        choice_standard["총합"] -= lecture_credit

                        delete_items.append(needcheck) 
                    break
    
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)


    ################################################### 검사 알고리즘 종료 ####################################################

    # print('일선으로 넘어갈 기이수과목 : ')
    # pprint.pprint(lectures_dict, width=80, sort_dicts=False)

    ###########################################################################################################################
    ################################################## 일반선택 및 학점계산 ###################################################


    rest_info = {"일반선택": [], "총합": Decimal(0.0)}

    if len(lectures_dict) > 0:
        for needcheck in lectures_dict[:]:
            lecture_credit = Decimal(needcheck['학점'])
            
            rest_info["일반선택"].append(needcheck)
            rest_info["총합"] += lecture_credit
        
    if rest != 0:
        rest_info["총합"] += rest

    # print('반영된 초과학점 : ', normal_later)
    
    lectures_dict.clear()


    if essential_GE_standard[0]["총합"] < 0:
        essential_GE_standard[0]["총합"] = 0   # 교필 부족한 영역 초기화

    lack_essential_GE = essential_GE_standard[0].pop('총합') # 교필 부족학점

    if chocie_GE_standard[0]["총합"] < 0:
        chocie_GE_standard[0]["총합"] = 0     # 교선 부족한 영역 초기화

    lack_choice_GE = chocie_GE_standard[0].pop('총합') # 교선 부족학점

    rest_total = rest_info["총합"] # 일선 총 이수학점


    # print("교필 부족한 영역:")
    # pprint.pprint(ness_result, width=80, sort_dicts=False)

    # print("교선 부족한 영역:")
    # pprint.pprint(choice_result, width=80, sort_dicts=False)

    # print("일반선택 과목:")
    # pprint.pprint(normal_total, width=80, sort_dicts=False)


    ################################################## 부족한 영역 및 학점 ###################################################


    lack_essential_GE_topic = essential_GE_standard[0] # 교필 부족 영역

    lack_choice_GE_topic = chocie_GE_standard[0] # 교선 부족 영역


    choice_keys_to_merge = ['고전탐구', '사유와지혜', '가치와실천', '상상력과표현', '인문융합']
    choice_new_key = '인간과문학, 역사와사회, 철학과예술'

    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in lack_choice_GE_topic for key in choice_keys_to_merge):
        lack_choice_GE_topic[choice_new_key] = sum(lack_choice_GE_topic.pop(key, Decimal('0')) for key in choice_keys_to_merge)

    balance1_keys_to_merge = ['균형1']
    balance1_new_key = '인간과문학, 언어와문화'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in lack_choice_GE_topic for key in balance1_keys_to_merge):
        lack_choice_GE_topic[balance1_new_key] = sum(lack_choice_GE_topic.pop(key, Decimal('0')) for key in balance1_keys_to_merge)

    balance2_keys_to_merge = ['균형2']
    balance2_new_key = '정치와경제, 역사와사회'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in lack_choice_GE_topic for key in balance2_keys_to_merge):
        lack_choice_GE_topic[balance2_new_key] = sum(lack_choice_GE_topic.pop(key, Decimal('0')) for key in balance2_keys_to_merge)

    balance3_keys_to_merge = ['균형3']
    balance3_new_key = '정보와기술, 자연과환경, 수리와과학'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in lack_choice_GE_topic for key in balance3_keys_to_merge):
        lack_choice_GE_topic[balance3_new_key] = sum(lack_choice_GE_topic.pop(key, Decimal('0')) for key in balance3_keys_to_merge)

    balance4_keys_to_merge = ['균형4']
    balance4_new_key = '심리와건강, 철학과예술'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in lack_choice_GE_topic for key in balance4_keys_to_merge):
        lack_choice_GE_topic[balance4_new_key] = sum(lack_choice_GE_topic.pop(key, Decimal('0')) for key in balance4_keys_to_merge)

    msc_keys_to_merge = ['MSC교과군']
    msc_new_key = '정보와기술, 자연과환경, 수리와과학'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in lack_essential_GE_topic for key in msc_keys_to_merge):
        lack_essential_GE_topic[msc_new_key] = sum(lack_essential_GE_topic.pop(key, Decimal('0')) for key in msc_keys_to_merge)

    lack_total_GE = lack_essential_GE + lack_choice_GE # 교양 종합 부족학점

    calculate_and_save_standard(done_GE, lack_total_GE, rest_total, student_id)

    result = {
        "lackEssentialGE": lack_essential_GE, #필수 부족학점
        "lackChoiceGE": lack_choice_GE, #선택 부족학점

        "lackEssentialGETopic": lack_essential_GE_topic, #필수 부족영역
        "lackChoiceGETopic": lack_choice_GE_topic, #선택 부족영역

        "doneEssentialGE": done_essential_GE, #필수 이수학점
        "doneChoiceGE": done_choice_GE, #선택 이수학점

        "doneGERest": rest_total, #일선 이수학점
    }
    return result

#사용자 교양 계산 학점 DB 저장
def calculate_and_save_standard(done_GE, lack_total_GE, rest_total, student_id):
    try:
        user = User.objects.get(student_id=student_id)
        
        if user.student_id != student_id:
            raise ValueError("user_id와 student_id가 일치하지 않습니다.")
        
        user.done_GE = done_GE
        user.lack_GE = lack_total_GE #부족한 교양 학점
        user.done_GE_rest = rest_total #교양 이수 일선 넘어가는 학점

        
        user.save()

    except User.DoesNotExist:
        print(f"사용자를 찾을 수 없습니다: {student_id}")
    except ValueError as ve:
        print(str(ve))
    except IntegrityError as ie:
        print(f"DB에 저장 중 오류 발생: {str(ie)}")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {str(e)}")