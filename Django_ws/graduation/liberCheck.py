from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import MyDoneLecture
from .models import liberRequire
from decimal import Decimal
import pprint

def check_db_mydone_liber(user_id):
    year = user_id[:4] 


    #기이수 과목에서 비교할 과목데이터 가져옴
    mydone_lecture_list = MyDoneLecture.objects.filter(user_id=user_id, lecture_type__in=['교양', '교선', '교필'])
    lectures_dict = []
    for lecture in mydone_lecture_list:
        lecture_data = {
            '교과목명': lecture.lecture_name,
            '주제': lecture.lecture_topic,
            '학점': lecture.credit
        }
        lectures_dict.append(lecture_data)

    print(f"사용자 {user_id}의 {year}년도 과목데이터:")

    print("넣기전 과목데이터:")
    pprint.pprint(lectures_dict, width=80, sort_dicts=False)


    #교양요건 테이블에서 비교할 연도 데이터 가져옴
    filtered_data = liberRequire.objects.filter(연도=year).values()
    ness_data = {'인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', 'MSC교과군', '철학적인간학', '신학적인간학'}
    choice_data = {'고전탐구', '사유와지혜', '가치와실천', '상상력과표현', '인문융합', '균형1', '균형2', '균형3', '균형4'}
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
    print("교양선택리스트:")
    pprint.pprint(choice_result, width=80, sort_dicts=False)

    ness_total = 0 #지우는거 대기
    nomal_total = 0




    delete_items = []

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
                    break

                elif lecture_credit == ness_credit:
                    del ness_item[lecture_topic]
                    ness_item['총합'] -= ness_credit

                    delete_items.append(needcheck)

                else:
                    break

        for choice_item in choice_result:
            if lecture_topic in choice_item:
                choice_credit = choice_item[lecture_topic]

                if lecture_credit < choice_credit:
                    missing_credit = choice_credit - lecture_credit
                    choice_item[lecture_topic] = missing_credit


                    delete_items.append(needcheck)

                    choice_item['총합'] -= lecture_credit

                elif lecture_credit > choice_credit:
                    break

                elif lecture_credit == choice_credit:
                    del choice_item[lecture_topic]
                    choice_item['총합'] -= choice_credit

                    delete_items.append(needcheck)

                else:
                    break

    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)


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
                    break

        if lecture_topic == "정보와기술":

            for choice_item in choice_result:
                if "균형3" in choice_item: 
                    choice_credit = choice_item["균형3"]

                    if lecture_credit == choice_credit:
                        del choice_item["균형3"]
                        choice_item["총합"] -= choice_credit

                        delete_items.append(needcheck) 
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

        if lecture_topic == "인간과문학":
            possible_topics = ["고전탐구", "사유와지혜", "가치와실천", "상상력과표현"]

            for choice_item in choice_result:
                for topic in possible_topics:  # '고전탐구' 등 확인
                    if topic in choice_item and choice_item[topic] > 0:  # 존재하는 경우
                        choice_credit = choice_item[topic]

                        if lecture_credit == choice_credit:  # 학점이 같다면 삭제
                            del choice_item[topic]
                            choice_item["총합"] -= choice_credit
                            delete_items.append(needcheck)
                            break  # 첫 번째로 찾은 항목을 삭제한 후 종료

        if lecture_topic == "역사와사회":
            possible_topics = ["고전탐구", "사유와지혜", "가치와실천", "상상력과표현"]

            for choice_item in choice_result:
                for topic in possible_topics:  # '고전탐구' 등 확인
                    if topic in choice_item and choice_item[topic] > 0:  # 존재하는 경우
                        choice_credit = choice_item[topic]

                        if lecture_credit == choice_credit:  # 학점이 같다면 삭제
                            del choice_item[topic]
                            choice_item["총합"] -= choice_credit
                            delete_items.append(needcheck)
                            break  # 첫 번째로 찾은 항목을 삭제한 후 종료

        if lecture_topic == "철학과예술":
            possible_topics = ["고전탐구", "사유와지혜", "가치와실천", "상상력과표현"]

            for choice_item in choice_result:
                for topic in possible_topics:  # '고전탐구' 등 확인
                    if topic in choice_item and choice_item[topic] > 0:  # 존재하는 경우
                        choice_credit = choice_item[topic]

                        if lecture_credit == choice_credit:  # 학점이 같다면 삭제
                            del choice_item[topic]
                            choice_item["총합"] -= choice_credit
                            delete_items.append(needcheck)
                            break  # 첫 번째로 찾은 항목을 삭제한 후 종료

        if lecture_topic == "인간과문학":
            possible_topics = ["인문융합"]

            for choice_item in choice_result:
                for topic in possible_topics:  # '고전탐구' 등 확인
                    if topic in choice_item and choice_item[topic] > 0:  # 존재하는 경우
                        choice_credit = choice_item[topic]

                        if lecture_credit == choice_credit:  # 학점이 같다면 삭제
                            del choice_item[topic]
                            choice_item["총합"] -= choice_credit
                            delete_items.append(needcheck)
                            break  # 첫 번째로 찾은 항목을 삭제한 후 종료

        if lecture_topic == "역사와사회":
            possible_topics = ["인문융합"]

            for choice_item in choice_result:
                for topic in possible_topics:  # '고전탐구' 등 확인
                    if topic in choice_item and choice_item[topic] > 0:  # 존재하는 경우
                        choice_credit = choice_item[topic]

                        if lecture_credit == choice_credit:  # 학점이 같다면 삭제
                            del choice_item[topic]
                            choice_item["총합"] -= choice_credit
                            delete_items.append(needcheck)
                            break  # 첫 번째로 찾은 항목을 삭제한 후 종료

        if lecture_topic == "철학과예술":
            possible_topics = ["인문융합"]

            for choice_item in choice_result:
                for topic in possible_topics:  # '고전탐구' 등 확인
                    if topic in choice_item and choice_item[topic] > 0:  # 존재하는 경우
                        choice_credit = choice_item[topic]

                        if lecture_credit == choice_credit:  # 학점이 같다면 삭제
                            del choice_item[topic]
                            choice_item["총합"] -= choice_credit
                            delete_items.append(needcheck)
                            break  # 첫 번째로 찾은 항목을 삭제한 후 종료


    for item in delete_items:
        if item in lectures_dict:
            lectures_dict.remove(item)

        

    print("남은 기이수 과목:")
    pprint.pprint(lectures_dict, width=80, sort_dicts=False)
    print("\n")
    print("남은 교양필수 과목:")
    pprint.pprint(ness_item, width=80, sort_dicts=False)
    print("남은 교양선택 과목:")
    pprint.pprint(choice_item, width=80, sort_dicts=False)
    print("일반선택 학점:", nomal_total)
            

    return {
        "total": ness_total,
    }
        

