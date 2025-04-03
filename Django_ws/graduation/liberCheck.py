import pprint
from django.db import IntegrityError
from decimal import Decimal
from user.models import User
from .models import MyDoneLecture
from graduation.models import Standard
from .models import liberRequire

def check_db_mydone_liber(user_id):
    student_id = user_id
    year = student_id[:4]   # 학번 전처리 (년도 추출)  ex) 2020xxxx > 2020


    ################################### 기이과목 목록 중 교양 과목 추출 (이수구분 : 교양, 교선, 교필) ###################################

    mydone_lecture_list = MyDoneLecture.objects.filter(user_id=student_id, lecture_type__in=['교양', '교선', '교필'])
    lectures_dict = []
    complete_liber_total_credit = 0
    complete_general_esse_credit = 0 
    complete_general_choice_credit = 0

    for lecture in mydone_lecture_list:
        lecture_data = {
            '교과목명': lecture.lecture_name,
            '주제': lecture.lecture_topic,
            '학점': lecture.credit
        }
        lectures_dict.append(lecture_data)

    for data in lectures_dict[:]:
        complete_liber_total_credit += data['학점'] # 교양과목 총 이수 학점

    for data in lectures_dict[:]:
        if data['주제'] in {'인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', 'MSC교과군', '철학적인간학', '신학적인간학'}:
            complete_general_esse_credit += data['학점']    # 교양필수 총 이수 학점
        else:
            complete_general_choice_credit += data['학점']  # 교양선택 총 이수 학점

    # print(f"{user_id} 학생 {year}년도 교양 기이수과목 데이터 : ")
    # pprint.pprint(lectures_dict, width=80, sort_dicts=False)



    ################################### 교양 교육과정 기준 학점 및 주제 추출 (18 ~ 22년도 : 트리니티 이전) ###################################

    filtered_data = liberRequire.objects.filter(연도=year).values()

    # 교양필수 주제 (18 ~ 22년도 : 트리니티 이전)
    ness_data = {'인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', 'MSC교과군', '철학적인간학', '신학적인간학'}
    
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

    # print("이수해야 하는 교필 기준 (주제 및 학점) : ")
    # pprint.pprint(ness_result[:], width=80, sort_dicts=False)

    # print("이수해야 하는 교선 기준 (주제 및 학점) : ")
    # pprint.pprint(choice_result[:], width=80, sort_dicts=False)


    ######################################################## 교필 영역 계산 ########################################################

    ######################### '인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩' ##########################
    #################################### '외국어', 'MSC교과군', '철학적인간학', '신학적인간학' #####################################

    delete_items = []
    normal_later = 0

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        for ness_item in ness_result:
            if lecture_topic in ness_item:
                ness_credit = ness_item[lecture_topic]

                if lecture_credit < ness_credit:
                    missing_credit = ness_credit - lecture_credit
                    ness_item[lecture_topic] = missing_credit

                    delete_items.append(needcheck)

                    ness_item['총합'] -= lecture_credit

                elif lecture_credit > ness_credit:
                    del ness_item[lecture_topic]
                    missing_credit = ness_credit - lecture_credit
                    normal_later = abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                    delete_items.append(needcheck)

                    ness_item['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                elif lecture_credit == ness_credit:
                    del ness_item[lecture_topic]
                    ness_item['총합'] -= ness_credit

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

        for choice_item in choice_result:
            if lecture_topic in choice_item:
                choice_credit = choice_item[lecture_topic]

                if lecture_credit < choice_credit:
                    missing_credit = choice_credit - lecture_credit
                    choice_item[lecture_topic] = missing_credit


                    delete_items.append(needcheck)

                    choice_item['총합'] -= lecture_credit

                elif lecture_credit > choice_credit:
                    del choice_item[lecture_topic]
                    missing_credit = lecture_credit - choice_credit
                    normal_later += missing_credit # 초과 학점 일반선택 학점 추가

                    delete_items.append(needcheck)
                    choice_item['총합'] -= choice_credit   # 학점 기준 초과 시 반영

                elif lecture_credit == choice_credit:
                    del choice_item[lecture_topic]
                    choice_item['총합'] -= choice_credit

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
            for ness_item in ness_result:
                if "MSC교과군" in ness_item and ness_item["MSC교과군"] > lecture_credit:
                    ness_credit = ness_item["MSC교과군"]
                    missing_credit = ness_credit - lecture_credit
                    ness_item["MSC교과군"] = missing_credit
                    ness_item["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "MSC교과군" in ness_item and ness_item["MSC교과군"] == lecture_credit: 
                    del ness_item["MSC교과군"]
                    delete_items.append(needcheck)
                    ness_item["총합"] -= lecture_credit

                elif "MSC교과군" in ness_item and ness_item["MSC교과군"] < lecture_credit: 
                    ness_credit = ness_item["MSC교과군"]
                    missing_credit = ness_credit - lecture_credit
                    normal_later += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del ness_item["MSC교과군"]
                    delete_items.append(needcheck)
                    
                    ness_item["총합"] -= choice_credit    # 학점 기준 초과 시 반영
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
            for ness_item in ness_result:
                if "창의적사고와코딩" in ness_item and ness_item["창의적사고와코딩"] > lecture_credit:
                    ness_credit = ness_item["창의적사고와코딩"]
                    missing_credit = ness_credit - lecture_credit
                    ness_item["창의적사고와코딩"] = missing_credit
                    ness_item["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "창의적사고와코딩" in ness_item and ness_item["창의적사고와코딩"] == lecture_credit: 
                    del ness_item["창의적사고와코딩"]
                    delete_items.append(needcheck)
                    ness_item["총합"] -= lecture_credit

                elif "창의적사고와코딩" in ness_item and ness_item["창의적사고와코딩"] < lecture_credit: 
                    ness_credit = ness_item["창의적사고와코딩"]
                    missing_credit = ness_credit - lecture_credit
                    normal_later += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del ness_item["창의적사고와코딩"]
                    delete_items.append(needcheck)
                    
                    ness_item["총합"] -= choice_credit    # 학점 기준 초과 시 반영
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

            for choice_item in choice_result:
                if "균형1" in choice_item: 
                    choice_credit = choice_item["균형1"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형1"]
                        choice_item["총합"] -= choice_credit

                        delete_items.append(needcheck) 
                    break
        
        if lecture_topic == "정치와경제":

            for choice_item in choice_result:
                if "균형2" in choice_item: 
                    choice_credit = choice_item["균형2"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형2"]
                        choice_item["총합"] -= choice_credit

                        delete_items.append(needcheck) 
                    
                    elif lecture_credit > choice_credit:
                        missing_credit = lecture_credit - choice_credit 
                        normal_later += missing_credit
                        del choice_item["균형2"]

                        delete_items.append(needcheck)

                        choice_item["총합"] -= choice_credit
                    break

        if lecture_topic == "정보와기술":

            for choice_item in choice_result:
                if "균형3" in choice_item: 
                    choice_credit = choice_item["균형3"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형3"]
                        choice_item["총합"] -= choice_credit

                        delete_items.append(needcheck)


                    elif lecture_credit > choice_credit:
                        missing_credit = lecture_credit - choice_credit 
                        normal_later += missing_credit
                        del choice_item["균형3"]

                        delete_items.append(needcheck)

                        choice_item["총합"] -= choice_credit
                    break

        if lecture_topic == "심리와건강":

            for choice_item in choice_result:
                if "균형4" in choice_item: 
                    choice_credit = choice_item["균형4"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형4"]
                        choice_item["총합"] -= choice_credit

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
            for choice_item in choice_result:
                if "고전탐구" in choice_item and choice_item["고전탐구"] == lecture_credit:
                    del choice_item["고전탐구"] 
                    choice_item["총합"] -= lecture_credit  
                    if needcheck not in delete_items:
                        delete_items.append(needcheck)
                    break
                
                if "사유와지혜" in choice_item and choice_item["사유와지혜"] == lecture_credit:
                    del choice_item["사유와지혜"] 
                    choice_item["총합"] -= lecture_credit
                    if needcheck not in delete_items:
                        delete_items.append(needcheck)
                    break

                if "가치와실천" in choice_item and choice_item["가치와실천"] == lecture_credit:
                    del choice_item["가치와실천"] 
                    choice_item["총합"] -= lecture_credit
                    if needcheck not in delete_items:
                        delete_items.append(needcheck)
                    break

                if "상상력과표현" in choice_item and choice_item["상상력과표현"] == lecture_credit:
                    del choice_item["상상력과표현"]
                    choice_item["총합"] -= lecture_credit
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
            for choice_item in choice_result:
                if "인문융합" in choice_item and choice_item["인문융합"] > lecture_credit:
                    choice_credit = choice_item["인문융합"]
                    missing_credit = choice_credit - lecture_credit
                    choice_item["인문융합"] = missing_credit
                    choice_item["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                elif "인문융합" in choice_item and choice_item["인문융합"] == lecture_credit: 
                    del choice_item["인문융합"]
                    delete_items.append(needcheck)
                    choice_item["총합"] -= lecture_credit  
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

            for choice_item in choice_result:
                if "균형1" in choice_item: 
                    choice_credit = choice_item["균형1"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형1"]
                        choice_item["총합"] -= lecture_credit

                        delete_items.append(needcheck) 
                    break
        
        if lecture_topic == "역사와사회":

            for choice_item in choice_result:
                if "균형2" in choice_item: 
                    choice_credit = choice_item["균형2"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형2"]
                        choice_item["총합"] -= lecture_credit

                        delete_items.append(needcheck) 
                    break

        if lecture_topic == "자연과환경":

            for choice_item in choice_result:
                if "균형3" in choice_item: 
                    choice_credit = choice_item["균형3"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형3"]
                        choice_item["총합"] -= lecture_credit

                        delete_items.append(needcheck) 
                    elif lecture_credit > choice_credit:
                        missing_credit = lecture_credit - choice_credit
                        normal_later += missing_credit
                        del choice_item["균형3"]

                        choice_item["총합"] -= choice_credit
                    break


        if lecture_topic == "수리와과학":

            for choice_item in choice_result:
                if "균형3" in choice_item: 
                    choice_credit = choice_item["균형3"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형3"]
                        choice_item["총합"] -= lecture_credit

                        delete_items.append(needcheck) 
                    elif lecture_credit > choice_credit:
                        missing_credit = lecture_credit - choice_credit
                        normal_later += missing_credit
                        del choice_item["균형3"]

                        choice_item["총합"] -= choice_credit
                    break


        if lecture_topic == "철학과예술":

            for choice_item in choice_result:
                if "균형4" in choice_item: 
                    choice_credit = choice_item["균형4"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형4"]
                        choice_item["총합"] -= lecture_credit

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


    normal_total = {"일반선택": [], "총합": Decimal(0.0)}

    if len(lectures_dict) > 0:
        for needcheck in lectures_dict[:]:
            lecture_credit = Decimal(needcheck['학점'])
            
            normal_total["일반선택"].append(needcheck)
            normal_total["총합"] += lecture_credit
        
    if normal_later != 0:
        normal_total["총합"] += normal_later

    # print('반영된 초과학점 : ', normal_later)
    
    lectures_dict.clear()


    if ness_result[0]["총합"] < 0:
        ness_result[0]["총합"] = 0   # 교필 부족한 영역 초기화

    need_general_esse_credit = ness_result[0].pop('총합') # 교필 부족학점

    if choice_result[0]["총합"] < 0:
        choice_result[0]["총합"] = 0     # 교선 부족한 영역 초기화

    need_general_choice_credit = choice_result[0].pop('총합') # 교선 부족학점

    total__normal_credit = normal_total["총합"] # 일선 총 이수학점


    # print("교필 부족한 영역:")
    # pprint.pprint(ness_result, width=80, sort_dicts=False)

    # print("교선 부족한 영역:")
    # pprint.pprint(choice_result, width=80, sort_dicts=False)

    # print("일반선택 과목:")
    # pprint.pprint(normal_total, width=80, sort_dicts=False)


    ################################################## 부족한 영역 및 학점 ###################################################


    need_general_esse_area = ness_result[0] # 교필 부족 영역

    need_general_choice_area = choice_result[0] # 교선 부족 영역


    choice_keys_to_merge = ['고전탐구', '사유와지혜', '가치와실천', '상상력과표현', '인문융합']
    choice_new_key = '인간과문학, 역사와사회, 철학과예술'

    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in need_general_choice_area for key in choice_keys_to_merge):
        need_general_choice_area[choice_new_key] = sum(need_general_choice_area.pop(key, Decimal('0')) for key in choice_keys_to_merge)

    balance1_keys_to_merge = ['균형1']
    balance1_new_key = '인간과문학, 언어와문화'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in need_general_choice_area for key in balance1_keys_to_merge):
        need_general_choice_area[balance1_new_key] = sum(need_general_choice_area.pop(key, Decimal('0')) for key in balance1_keys_to_merge)

    balance2_keys_to_merge = ['균형2']
    balance2_new_key = '정치와경제, 역사와사회'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in need_general_choice_area for key in balance2_keys_to_merge):
        need_general_choice_area[balance2_new_key] = sum(need_general_choice_area.pop(key, Decimal('0')) for key in balance2_keys_to_merge)

    balance3_keys_to_merge = ['균형3']
    balance3_new_key = '정보와기술, 자연과환경, 수리와과학'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in need_general_choice_area for key in balance3_keys_to_merge):
        need_general_choice_area[balance3_new_key] = sum(need_general_choice_area.pop(key, Decimal('0')) for key in balance3_keys_to_merge)

    balance4_keys_to_merge = ['균형4']
    balance4_new_key = '심리와건강, 철학과예술'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in need_general_choice_area for key in balance4_keys_to_merge):
        need_general_choice_area[balance4_new_key] = sum(need_general_choice_area.pop(key, Decimal('0')) for key in balance4_keys_to_merge)

    msc_keys_to_merge = ['MSC교과군']
    msc_new_key = '정보와기술, 자연과환경, 수리와과학'
    # 해당 키들 중 하나라도 존재하면 값을 합산하고 새로운 키에 할당
    if any(key in need_general_esse_area for key in msc_keys_to_merge):
        need_general_esse_area[msc_new_key] = sum(need_general_esse_area.pop(key, Decimal('0')) for key in msc_keys_to_merge)

    need_liber_total_credit = need_general_esse_credit + need_general_choice_credit # 교양 종합 부족학점

    calculate_and_save_standard(complete_liber_total_credit, need_liber_total_credit, total__normal_credit, student_id)

    result = {
        "교양필수 부족 학점": need_general_esse_credit, #필수 부족학점
        "교양선택 부족 학점": need_general_choice_credit, #선택 부족학점

        "교양필수 부족 영역": need_general_esse_area, #필수 부족영역
        "교양선택 부족 영역": need_general_choice_area, #선택 부족영역

        "교양필수 이수 학점": complete_general_esse_credit, #필수 이수학점
        "교양선택 이수 학점": complete_general_choice_credit, #선택 이수학점

        "일반선택 이수 학점": total__normal_credit, #일선 이수학점
    }
    return result


def calculate_and_save_standard(complete_liber, need_liber, complete_normal, student_id):
    try:
        user = User.objects.get(student_id=student_id)
        
        if user.student_id != student_id:
            raise ValueError("user_id와 student_id가 일치하지 않습니다.")
        
        user.done_general = complete_liber
        user.need_general = need_liber
        user.done_general_rest = complete_normal

        
        user.save()

    except User.DoesNotExist:
        print(f"사용자를 찾을 수 없습니다: {student_id}")
    except ValueError as ve:
        print(str(ve))
    except IntegrityError as ie:
        print(f"DB에 저장 중 오류 발생: {str(ie)}")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {str(e)}")