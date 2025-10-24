from user.models import User
from .GE_calculate import get_user_GE
from .GE_calculate import get_user_GE_standard
from .GE_calculate import find_user_college
from .GE_calculate import calculate_and_save_standard
from decimal import Decimal

#교양 인성 계산
def GE_humanism_calculate(lecture_dict, user_GE_standard):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['humanism_GE_standard'] #[{'인간학': Decimal('4.0'), '트리니티아카데미': Decimal('2.0'), '총합': Decimal('6.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = 0

    lecture_check = []


    #교양 인성 인간학, 봉사활동, VERUM캠프 계산(주제가 DB의 교양요건과 동일한 경우)
    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        for GE_standard in user_GE_standard:
            if lecture_topic in GE_standard:
                lecture_update = needcheck.copy()
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

    #삭제명단에 오른 과목 데이터 삭제
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    return lectures_dict, user_GE_standard, rest_total, lecture_check

#교양 융합 계산
def GE_fusion_calculate(lecture_dict, user_GE_standard, rest_total, GE_humanism_standard):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['fusion_GE_standard'] #[{'정보활용': Decimal('6.0'), '창의융합': Decimal('6.0'), '문제해결': Decimal('6.0'), '총합': Decimal('18.0')}]
    GE_humanism_standard = GE_humanism_standard
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = rest_total

    lecture_check = []

    for needcheck in lectures_dict[:]:
        lecture_topic = needcheck['주제']
        lecture_credit = Decimal(needcheck['학점'])

        #각 영역이 사용자가 들은 과목에 들어가 있다면 해당 영역의 교양요건 계산 (정보활용)
        if lecture_topic in ["정치와경제"]:

            for GE_standard in user_GE_standard:
                if "정보활용" in GE_standard and GE_standard["정보활용"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["정보활용"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '정보활용'
                    lecture_check.append(lecture_update)

                elif "정보활용" in GE_standard and GE_standard["정보활용"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '정보활용'
                    lecture_check.append(lecture_update)

                elif "정보활용" in GE_standard and GE_standard["정보활용"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) 
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))

                    lecture_update['분류'] = '정보활용'
                    lecture_check.append(lecture_update)

                else:
                    continue

        if lecture_topic in ["심리와건강"]:

            for GE_standard in user_GE_standard:
                if "정보활용" in GE_standard and GE_standard["정보활용"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["정보활용"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '정보활용'
                    lecture_check.append(lecture_update)

                elif "정보활용" in GE_standard and GE_standard["정보활용"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '정보활용'
                    lecture_check.append(lecture_update)

                elif "정보활용" in GE_standard and GE_standard["정보활용"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) 
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))   

                    lecture_update['분류'] = '정보활용'
                    lecture_check.append(lecture_update)

                else:
                    continue

        if lecture_topic in ["정보와기술"]:

            for GE_standard in user_GE_standard:
                if "정보활용" in GE_standard and GE_standard["정보활용"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["정보활용"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '정보활용'
                    lecture_check.append(lecture_update)

                elif "정보활용" in GE_standard and GE_standard["정보활용"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '정보활용'
                    lecture_check.append(lecture_update)

                elif "정보활용" in GE_standard and GE_standard["정보활용"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["정보활용"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)
                    del GE_standard["정보활용"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))   

                    lecture_update['분류'] = '정보활용'
                    lecture_check.append(lecture_update)

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

            for GE_standard in user_GE_standard:
                if "창의융합" in GE_standard and GE_standard["창의융합"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["창의융합"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '창의융합'
                    lecture_check.append(lecture_update)

                elif "창의융합" in GE_standard and GE_standard["창의융합"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '창의융합'
                    lecture_check.append(lecture_update)

                elif "창의융합" in GE_standard and GE_standard["창의융합"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) 
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))   

                    lecture_update['분류'] = '창의융합'
                    lecture_check.append(lecture_update)

                else:
                    continue

        if lecture_topic in ["역사와사회"]:

            for GE_standard in user_GE_standard:
                if "창의융합" in GE_standard and GE_standard["창의융합"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["창의융합"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '창의융합'
                    lecture_check.append(lecture_update)

                elif "창의융합" in GE_standard and GE_standard["창의융합"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '창의융합'
                    lecture_check.append(lecture_update)

                elif "창의융합" in GE_standard and GE_standard["창의융합"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) 
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))  

                    lecture_update['분류'] = '창의융합'
                    lecture_check.append(lecture_update)

                else:
                    continue

        if lecture_topic in ["철학과예술"]:

            for GE_standard in user_GE_standard:
                if "창의융합" in GE_standard and GE_standard["창의융합"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["창의융합"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '창의융합'
                    lecture_check.append(lecture_update)

                elif "창의융합" in GE_standard and GE_standard["창의융합"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '창의융합'
                    lecture_check.append(lecture_update)

                elif "창의융합" in GE_standard and GE_standard["창의융합"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["창의융합"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)
                    del GE_standard["창의융합"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit)) 

                    lecture_update['분류'] = '창의융합'
                    lecture_check.append(lecture_update)

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

            for GE_standard in user_GE_standard:
                if "문제해결" in GE_standard and GE_standard["문제해결"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["문제해결"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '문제해결'
                    lecture_check.append(lecture_update)

                elif "문제해결" in GE_standard and GE_standard["문제해결"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '문제해결'
                    lecture_check.append(lecture_update)

                elif "문제해결" in GE_standard and GE_standard["문제해결"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))

                    lecture_update['분류'] = '문제해결'
                    lecture_check.append(lecture_update)

                else:
                    continue

        if lecture_topic in ["수리와과학"]:

            for GE_standard in user_GE_standard:
                if "문제해결" in GE_standard and GE_standard["문제해결"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["문제해결"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '문제해결'
                    lecture_check.append(lecture_update)

                elif "문제해결" in GE_standard and GE_standard["문제해결"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '문제해결'
                    lecture_check.append(lecture_update)

                elif "문제해결" in GE_standard and GE_standard["문제해결"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))   

                    lecture_update['분류'] = '문제해결'
                    lecture_check.append(lecture_update)

                else:
                    continue

        if lecture_topic in ["언어와문화"]:

            for GE_standard in user_GE_standard:
                if "문제해결" in GE_standard and GE_standard["문제해결"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["문제해결"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '문제해결'
                    lecture_check.append(lecture_update)

                elif "문제해결" in GE_standard and GE_standard["문제해결"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '문제해결'
                    lecture_check.append(lecture_update)

                elif "문제해결" in GE_standard and GE_standard["문제해결"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["문제해결"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["문제해결"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = '문제해결'
                    lecture_check.append(lecture_update)

                else:
                    continue

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    #각 영역이 사용자가 들은 과목에 들어가 있다면 해당 영역의 교양요건 계산 (융합비고) => 교양 요건에 융합비고가 있는 경우에만 작동
    for GE_standard in user_GE_standard:
        if '융합비고' in GE_standard:

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

                    for GE_standard in user_GE_standard:
                        if "융합비고" in GE_standard and GE_standard["융합비고"] > lecture_credit:
                            lecture_update = needcheck.copy()
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            GE_standard["융합비고"] = missing_credit
                            GE_standard["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                            lecture_update['분류'] = '융합비고'
                            lecture_check.append(lecture_update)

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] == lecture_credit: 
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            GE_standard["총합"] -= lecture_credit

                            lecture_update['분류'] = '융합비고'
                            lecture_check.append(lecture_update)

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] < lecture_credit: 
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            
                            GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                            lecture_update['분류'] = '융합비고'
                            lecture_check.append(lecture_update)

                        else:
                            continue

                if lecture_topic in ["인간과문학", "역사와사회", "철학과예술"]:

                    if len(stack_fusion) == 0:
                        stack_fusion.append(1)
                    else:
                        continue

                    for GE_standard in user_GE_standard:
                        if "융합비고" in GE_standard and GE_standard["융합비고"] > lecture_credit:
                            lecture_update = needcheck.copy()
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            GE_standard["융합비고"] = missing_credit
                            GE_standard["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                            lecture_update['분류'] = '융합비고'
                            lecture_check.append(lecture_update)

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] == lecture_credit: 
                            lecture_update = needcheck.copy()
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            GE_standard["총합"] -= lecture_credit

                            lecture_update['분류'] = '융합비고'
                            lecture_check.append(lecture_update)

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] < lecture_credit: 
                            lecture_update = needcheck.copy()
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            
                            GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                            lecture_update['분류'] = '융합비고'
                            lecture_check.append(lecture_update)

                        else:
                            continue

                if lecture_topic in ["자연과환경", "수리와과학", "언어와문화"]:

                    if len(stack_problem) == 0:
                        stack_problem.append(1)
                    else:
                        continue

                    for GE_standard in user_GE_standard:
                        if "융합비고" in GE_standard and GE_standard["융합비고"] > lecture_credit:
                            lecture_update = needcheck.copy()
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            GE_standard["융합비고"] = missing_credit
                            GE_standard["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                            lecture_update['분류'] = '융합비고'
                            lecture_check.append(lecture_update)

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] == lecture_credit: 
                            lecture_update = needcheck.copy()
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            GE_standard["총합"] -= lecture_credit

                            lecture_update['분류'] = '융합비고'
                            lecture_check.append(lecture_update)

                        elif "융합비고" in GE_standard and GE_standard["융합비고"] < lecture_credit: 
                            lecture_update = needcheck.copy()
                            GE_credit = GE_standard["융합비고"]
                            missing_credit = GE_credit - lecture_credit
                            rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del GE_standard["융합비고"]
                            delete_items.append(needcheck)
                            
                            GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                            lecture_update['분류'] = '융합비고'
                            lecture_check.append(lecture_update)

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

    #23년도 트리니티아카데미 대체과목 계산 로직 (트리니티아카데미가 있을 경우에만)
    for GE_standard in GE_humanism_standard:
        if '트리니티아카데미' in GE_standard:
            for needcheck in lectures_dict[:]:
                lecture_topic = needcheck['주제']
                lecture_credit = Decimal(needcheck['학점'])

                #대체과목 영역이 사용자 교양 들은 과목에 존재한다면 트리니티아카데미를 계산한다
                if lecture_topic in ["정치와경제", "심리와건강", "정보와기술", "인간과문학", "역사와사회", "철학과예술", "자연과환경", "수리와과학", "언어와문화"]:
                    for GE_standard in user_GE_standard:
                        if "트리니티아카데미" in GE_standard and GE_standard["트리니티아카데미"] > lecture_credit:
                            lecture_update = needcheck.copy()
                            GE_credit = GE_standard["트리니티아카데미"]
                            missing_credit = GE_credit - lecture_credit
                            GE_standard["트리니티아카데미"] = missing_credit
                            GE_standard["총합"] -= lecture_credit
                            delete_items.append(needcheck)

                            lecture_update['분류'] = '트리니티아카데미'
                            lecture_check.append(lecture_update)                           

                        elif "트리니티아카데미" in GE_standard and GE_standard["트리니티아카데미"] == lecture_credit: 
                            lecture_update = needcheck.copy()
                            del GE_standard["트리니티아카데미"]
                            delete_items.append(needcheck)
                            GE_standard["총합"] -= lecture_credit

                            lecture_update['분류'] = '트리니티아카데미'
                            lecture_check.append(lecture_update)    

                        elif "트리니티아카데미" in GE_standard and GE_standard["트리니티아카데미"] < lecture_credit: 
                            lecture_update = needcheck.copy()
                            GE_credit = GE_standard["트리니티아카데미"]
                            missing_credit = GE_credit - lecture_credit
                            rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                            del GE_standard["트리니티아카데미"]
                            delete_items.append(needcheck)
                            
                            GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                            lecture_update['분류'] = '트리니티아카데미'
                            lecture_check.append(lecture_update)    

                        else:
                            break
        else:
            break


    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    return lectures_dict, user_GE_standard, rest_total, GE_humanism_standard, lecture_check

#23년도 교양 기초 계산
def GE_basic_calculate_2023(lecture_dict, user_GE_standard, user_college, rest_total):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['basic_GE_standard'] #[{'논리적사고와글쓰기': Decimal('2.0'), '외국어': Decimal('4.0'), '자기관리': Decimal('6.0'), '총합': Decimal('12.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = rest_total

    lecture_check = []

    #계열기초
    stack_major_base = []
    #창의성
    stack_creative = []
    #창업
    stack_startup = []
    #진로탐색
    stack_search = []

    # 트리니티자유대학
    if (user_college == 'trinity'):
        for needcheck in lectures_dict[:]:
            lecture_topic = needcheck['주제']
            lecture_credit = Decimal(needcheck['학점'])

            for GE_standard in user_GE_standard:
                if lecture_topic in GE_standard:
                    GE_credit = GE_standard[lecture_topic]

                    if lecture_credit < GE_credit:
                        lecture_update = needcheck.copy()
                        missing_credit = GE_credit - lecture_credit
                        GE_standard[lecture_topic] = missing_credit

                        delete_items.append(needcheck)

                        GE_standard['총합'] -= lecture_credit

                        lecture_update['분류'] = lecture_topic
                        lecture_check.append(lecture_update)

                    elif lecture_credit > GE_credit:
                        lecture_update = needcheck.copy()
                        del GE_standard[lecture_topic]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                        delete_items.append(needcheck)

                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                        lecture_update['분류'] = lecture_topic
                        lecture_check.append(lecture_update)

                    elif lecture_credit == GE_credit:
                        lecture_update = needcheck.copy()
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
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                        lecture_update['분류'] = '창의성'
                        lecture_check.append(lecture_update)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        lecture_update = needcheck.copy()
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                        lecture_update['분류'] = '창의성'
                        lecture_check.append(lecture_update)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                        lecture_update['분류'] = '창의성'
                        lecture_check.append(lecture_update)

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
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                        lecture_update['분류'] = '창업'
                        lecture_check.append(lecture_update)                        

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        lecture_update = needcheck.copy()
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                        lecture_update['분류'] = '창업'
                        lecture_check.append(lecture_update)  

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                        lecture_update['분류'] = '창업'
                        lecture_check.append(lecture_update)  

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
                    if lecture_credit == 2:
                        stack_search.append(1)
                        stack_search.append(1)
                    else:
                        stack_search.append(1)
                elif len(stack_search) == 1:
                    if lecture_credit == 2:
                        stack_search.append(1)
                        stack_search.append(1)
                    else:
                        stack_search.append(1)
                elif len(stack_search) == 2:
                    if lecture_credit == 2:
                        stack_search.append(1)
                        stack_search.append(1)
                    else:
                        stack_search.append(1)
                else:
                    continue

                for GE_standard in user_GE_standard:
                    if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                        lecture_update['분류'] = '진로탐색'
                        lecture_check.append(lecture_update)  

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        lecture_update = needcheck.copy()
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                        lecture_update['분류'] = '진로탐색'
                        lecture_check.append(lecture_update)  

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                        lecture_update['분류'] = '진로탐색'
                        lecture_check.append(lecture_update)  

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
                        lecture_update = needcheck.copy()
                        missing_credit = GE_credit - lecture_credit
                        GE_standard[lecture_topic] = missing_credit

                        delete_items.append(needcheck)

                        GE_standard['총합'] -= lecture_credit

                        lecture_update['분류'] = lecture_topic
                        lecture_check.append(lecture_update)  

                    elif lecture_credit > GE_credit:
                        lecture_update = needcheck.copy()
                        del GE_standard[lecture_topic]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                        delete_items.append(needcheck)

                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                        lecture_update['분류'] = lecture_topic
                        lecture_check.append(lecture_update)  

                    elif lecture_credit == GE_credit:
                        lecture_update = needcheck.copy()
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
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                        lecture_update['분류'] = '계열기초'
                        lecture_check.append(lecture_update) 

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        lecture_update = needcheck.copy()
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                        lecture_update['분류'] = '계열기초'
                        lecture_check.append(lecture_update) 

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                        lecture_update['분류'] = '계열기초'
                        lecture_check.append(lecture_update) 

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
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                        lecture_update['분류'] = '창의성'
                        lecture_check.append(lecture_update) 

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        lecture_update = needcheck.copy()
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                        lecture_update['분류'] = '창의성'
                        lecture_check.append(lecture_update) 

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                        lecture_update['분류'] = '창의성'
                        lecture_check.append(lecture_update) 

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
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                        lecture_update['분류'] = '창업'
                        lecture_check.append(lecture_update)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        lecture_update = needcheck.copy()
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                        lecture_update['분류'] = '창업'
                        lecture_check.append(lecture_update)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                        lecture_update['분류'] = '창업'
                        lecture_check.append(lecture_update)

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
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        GE_standard["자기관리"] = missing_credit
                        GE_standard["총합"] -= lecture_credit
                        delete_items.append(needcheck)

                        lecture_update['분류'] = '진로탐색'
                        lecture_check.append(lecture_update)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                        lecture_update = needcheck.copy()
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        GE_standard["총합"] -= lecture_credit

                        lecture_update['분류'] = '진로탐색'
                        lecture_check.append(lecture_update)

                    elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                        lecture_update = needcheck.copy()
                        GE_credit = GE_standard["자기관리"]
                        missing_credit = GE_credit - lecture_credit
                        rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                        del GE_standard["자기관리"]
                        delete_items.append(needcheck)
                        
                        GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                        lecture_update['분류'] = '진로탐색'
                        lecture_check.append(lecture_update)

                    else:
                        break
                    
        for item in delete_items:
            if item in lectures_dict:
                lectures_dict.remove(item)
        delete_items = []

    return lectures_dict, user_GE_standard, rest_total, stack_major_base, stack_creative, stack_startup, stack_search, lecture_check

#24, 25년도 교양 기초 계산
def GE_basic_calculate_2025(lecture_dict, user_GE_standard, rest_total):
    lectures_dict = [] #매개변수 담을 리스트
    user_GE_standard = user_GE_standard['basic_GE_standard'] #[{'논리적사고와글쓰기': Decimal('2.0'), '외국어': Decimal('4.0'), '자기관리': Decimal('6.0'), '총합': Decimal('12.0')}]
    lectures_dict = lecture_dict #기이수 과목목록

    delete_items = []
    rest_total = rest_total

    lecture_check = []

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
                    lecture_update = needcheck.copy()
                    missing_credit = GE_credit - lecture_credit
                    GE_standard[lecture_topic] = missing_credit

                    delete_items.append(needcheck)

                    GE_standard['총합'] -= lecture_credit

                    lecture_update['분류'] = lecture_topic
                    lecture_check.append(lecture_update)

                elif lecture_credit > GE_credit:
                    lecture_update = needcheck.copy()
                    del GE_standard[lecture_topic]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit)  # 초과 학점 일반선택 학점 추가

                    delete_items.append(needcheck)

                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = lecture_topic
                    lecture_check.append(lecture_update)

                elif lecture_credit == GE_credit:
                    lecture_update = needcheck.copy()
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
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["소통"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["소통"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '논리적사고와글쓰기'
                    lecture_check.append(lecture_update)

                elif "소통" in GE_standard and GE_standard["소통"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["소통"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '논리적사고와글쓰기'
                    lecture_check.append(lecture_update)

                elif "소통" in GE_standard and GE_standard["소통"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["소통"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["소통"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = '논리적사고와글쓰기'
                    lecture_check.append(lecture_update)

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
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["소통"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["소통"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '외국어'
                    lecture_check.append(lecture_update)                    

                elif "소통" in GE_standard and GE_standard["소통"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["소통"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '외국어'
                    lecture_check.append(lecture_update)    

                elif "소통" in GE_standard and GE_standard["소통"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["소통"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["소통"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = '외국어'
                    lecture_check.append(lecture_update)  

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
            elif len(stack_major_base) == 1:
                stack_major_base.append(1)
            elif len(stack_major_base) == 2:
                stack_major_base.append(1)      
            else:
                continue

            for GE_standard in user_GE_standard:
                if "자기관리" in GE_standard and GE_standard["자기관리"] > lecture_credit:
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["자기관리"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '계열기초'
                    lecture_check.append(lecture_update) 

                elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '계열기초'
                    lecture_check.append(lecture_update) 

                elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = '계열기초'
                    lecture_check.append(lecture_update) 

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
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["자기관리"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '창의성'
                    lecture_check.append(lecture_update) 

                elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '창의성'
                    lecture_check.append(lecture_update) 

                elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = '창의성'
                    lecture_check.append(lecture_update) 

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
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["자기관리"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '창업'
                    lecture_check.append(lecture_update) 

                elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '창업'
                    lecture_check.append(lecture_update)

                elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = '창업'
                    lecture_check.append(lecture_update)

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
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    GE_standard["자기관리"] = missing_credit
                    GE_standard["총합"] -= lecture_credit
                    delete_items.append(needcheck)

                    lecture_update['분류'] = '진로탐색'
                    lecture_check.append(lecture_update)                    

                elif "자기관리" in GE_standard and GE_standard["자기관리"] == lecture_credit: 
                    lecture_update = needcheck.copy()
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    GE_standard["총합"] -= lecture_credit

                    lecture_update['분류'] = '진로탐색'
                    lecture_check.append(lecture_update)

                elif "자기관리" in GE_standard and GE_standard["자기관리"] < lecture_credit: 
                    lecture_update = needcheck.copy()
                    GE_credit = GE_standard["자기관리"]
                    missing_credit = GE_credit - lecture_credit
                    rest_total += abs(missing_credit) # 초과 학점 일반선택 학점 추가
                    del GE_standard["자기관리"]
                    delete_items.append(needcheck)
                    
                    GE_standard['총합'] -= (lecture_credit - abs(missing_credit))    # 학점 기준 초과 시 반영

                    lecture_update['분류'] = '진로탐색'
                    lecture_check.append(lecture_update)

                else:
                    break
                
    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)
    delete_items = []

    return lectures_dict, user_GE_standard, rest_total, stack_major_base, stack_creative, stack_startup, stack_search, stack_write, lecture_check

#일반선택 학점, 교양 이수 학점 계산 후 result로 전달
def rest_and_done_calculate(GE_total, lecture_dict_result, rest_total):
    done_humanism_GE = GE_total['done_humanism_GE']
    done_basic_GE = GE_total['done_basic_GE']
    done_fusion_GE = GE_total['done_fusion_GE']

    #일선학점 계산
    rest_total_last = Decimal('0.0')
    for item in lecture_dict_result:
        rest_total_last += item['학점']

    rest_total_topic = rest_total_last + rest_total

    return done_humanism_GE, done_basic_GE, done_fusion_GE, rest_total_topic

#교양 부족학점, 부족 영역 계산
def lack_GE_calculate(GE_humanism_standard, GE_fusion_standard, GE_basic_standard):
    lack_GE_humanism_total = GE_humanism_standard[0]['총합']
    lack_GE_fusion_total = GE_fusion_standard[0]['총합']
    lack_GE_basic_total = GE_basic_standard[0]['총합']

    return lack_GE_humanism_total, lack_GE_fusion_total, lack_GE_basic_total

#트리티니 교양 계산 컨트롤타워
def GE_trinity_calculate(user_id):
    year = user_id[:4]

    user_major = User.objects.filter(student_id=user_id).values('major').first()

    #소속 단과대학 추출
    user_college = find_user_college(user_major)
    print(f"소속대학: {user_college}")

    #전체과목 데이터 추출
    lecture_dict, GE_total = get_user_GE(user_id)
    
    #사용자 교양요건 추출
    user_GE_standard = get_user_GE_standard(year, user_college)

    print(f"교양 인성 기준: {user_GE_standard['humanism_GE_standard'][0]}")
    print(f"교양 기초 기준: {user_GE_standard['basic_GE_standard'][0]}")
    print(f"교양 융합 기준: {user_GE_standard['fusion_GE_standard'][0]}")
        
    lecture_dict_result, GE_humanism_standard, rest_total, GE_humanism_lecture_check = GE_humanism_calculate(lecture_dict, user_GE_standard)


    lecture_dict_result, GE_fusion_standard, rest_total, GE_humanism_standard, GE_fusion_lecture_check = GE_fusion_calculate(lecture_dict_result, user_GE_standard, rest_total, GE_humanism_standard)


    if (year == '2023'):
        #23년도 교양기초일때에만 다른 연도와 분리된 함수 사용
        lecture_dict_result, GE_basic_standard, rest_total, stack_major_base, stack_creative, stack_startup, stack_search, GE_basic_lecture_check = GE_basic_calculate_2023(lecture_dict_result, user_GE_standard, user_college, rest_total)

    else:
        #23년도가 아닐떄에는 기존 교양기초 함수 사용
        lecture_dict_result, GE_basic_standard, rest_total, stack_major_base, stack_creative, stack_startup, stack_search, stack_write, GE_basic_lecture_check = GE_basic_calculate_2025(lecture_dict_result, user_GE_standard, rest_total)


    #일반선택 학점 및 교양 이수 학점 계산
    done_humanism_GE, done_basic_GE, done_fusion_GE, rest_total_topic = rest_and_done_calculate(GE_total, lecture_dict_result, rest_total)

    print(f"부족 영역(교양 인성): {GE_humanism_standard[0]}")
    print(f"부족 영역(교양 기초): {GE_basic_standard[0]}")
    print(f"부족 영역(교양 융합): {GE_fusion_standard[0]}")

    #최종 일반선택 학점 = 로직 후 일반선택 학점 + 남은 교양과목 총합
    rest_total = rest_total_topic
    print(f'교양 > 일선 학점: {rest_total}\n')

    #교양 부족 학점
    lack_GE_humanism_total, lack_GE_fusion_total, lack_GE_basic_total = lack_GE_calculate(GE_humanism_standard, GE_fusion_standard, GE_basic_standard)

    lack_GE_humanism_topic = GE_humanism_standard[0]
    lack_GE_fusion_topic = GE_fusion_standard[0]
    lack_GE_basic_topic = GE_basic_standard[0]

    #총합 제거
    lack_GE_humanism_topic.pop('총합')
    lack_GE_fusion_topic.pop('총합')
    lack_GE_basic_topic.pop('총합')

    changed_lack_GE_humanism_topic = {}

    for key in lack_GE_humanism_topic:
        if 'VERUM캠프' in key and int(year) > 2022:
            new_key = key.replace('VERUM캠프', 'VERUM인성')
            changed_lack_GE_humanism_topic[new_key] = lack_GE_humanism_topic[key]
        else:
            changed_lack_GE_humanism_topic[key] = lack_GE_humanism_topic[key]

    #교양 기초 소분류 제목으로 변경
    changed_lack_GE_basic_topic = {}
    for key in lack_GE_basic_topic:
        if key == '자기관리':
    
            if year == '2023':
                 #23학번 일반학과
                if user_college == 'trinity':
                    new_key = '진로탐색, 창의성, 창업'
                    excluded = []

                    if len(stack_search) == 2:
                        excluded.append('진로탐색')
                    if len(stack_creative) == 1:
                        excluded.append('창의성')
                    if len(stack_startup) == 1:
                        excluded.append('창업')
                    
                    topic = ['진로탐색', '창의성', '창업']
                    topic = [t for t in topic if t not in excluded]
                    new_key = ', '.join(topic)

                #23학번 휴먼서비스, 의과대학
                else:
                    new_key = '진로탐색, 창의성, 창업'
                    excluded = []

                    if len(stack_search) == 2:
                        excluded.append('진로탐색')
                    if len(stack_creative) == 1:
                        excluded.append('창의성')
                    if len(stack_startup) == 1:
                        excluded.append('창업')
                    
                    topic = ['진로탐색', '창의성', '창업']
                    topic = [t for t in topic if t not in excluded]
                    new_key = ', '.join(topic)

            #24, 25학번
            else:
                    new_key = '진로탐색, 창의성, 창업, 계열기초'
                    excluded = []

                    if len(stack_search) == 2:
                        excluded.append('진로탐색')
                    if len(stack_creative) == 1:
                        excluded.append('창의성')
                    if len(stack_startup) == 1:
                        excluded.append('창업')
                    if len(stack_major_base) == 3:
                        excluded.append('계열기초')
                    
                    topic = ['진로탐색', '창의성', '창업', '계열기초']
                    topic = [t for t in topic if t not in excluded]
                    new_key = ', '.join(topic)

            changed_lack_GE_basic_topic[new_key] = lack_GE_basic_topic[key]

        elif key == '소통':
            new_key = '논리적사고와글쓰기, 외국어'
            excluded = []

            if len(stack_write) == 1:
                excluded.append('논리적사고와글쓰기')
            
            topic = ['논리적사고와글쓰기', '외국어']
            topic = [t for t in topic if t not in excluded]
            new_key = ', '.join(topic)

            changed_lack_GE_basic_topic[new_key] = lack_GE_basic_topic[key]

        else:
            changed_lack_GE_basic_topic[key] = lack_GE_basic_topic[key]

    #교양 융합 소분류 제목으로 변경
    changed_lack_GE_fusion_topic = {}
    for key in lack_GE_fusion_topic:
        if '정보활용' in key:
            changed_lack_GE_fusion_topic['정치와경제, 심리와건강, 정보와기술'] = lack_GE_fusion_topic[key]
        elif '창의융합' in key:
            changed_lack_GE_fusion_topic['인간과문학, 역사와사회, 철학과예술'] = lack_GE_fusion_topic[key]
        elif '문제해결' in key:
            changed_lack_GE_fusion_topic['자연과환경, 수리와과학, 언어와문화'] = lack_GE_fusion_topic[key]

    #교양 인성, 기초 => 교양 필수로 병합
    lack_GE_essential_topic = changed_lack_GE_humanism_topic | changed_lack_GE_basic_topic | changed_lack_GE_fusion_topic


    #DB에 저장할 교양 이수 학점, 교양 부족 학점, 일반선택 학점, 학번
    done_GE = GE_total['done_GE']
    lack_total_GE = lack_GE_humanism_total + lack_GE_basic_total + lack_GE_fusion_total

    #DB에 저장할 교양 세부 검사 과정
    GE_lecture_check = GE_basic_lecture_check + GE_fusion_lecture_check + GE_humanism_lecture_check

    #DB에 저장
    calculate_and_save_standard(done_GE, lack_total_GE, rest_total, user_id, GE_lecture_check)

    data = {
            'lackEssentialGE': lack_total_GE,
            'lackChoiceGE': None, 

            'lackEssentialGETopic': lack_GE_essential_topic, 
            'lackChoiceGETopic': None, 

            'doneEssentialGE': done_humanism_GE + done_basic_GE + done_fusion_GE, 
            'doneChoiceGE': None, 

            'doneGERest': rest_total, 
    }

    return data