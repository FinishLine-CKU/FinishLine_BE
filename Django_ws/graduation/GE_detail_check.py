from user.models import User
from .GE_calculate import find_user_college
from .GE_calculate import get_user_GE_standard
from .models import MyDoneLecture
def GE_detail_check(user_id):
    
    student_year = user_id[:4]
    user_major = User.objects.filter(student_id=user_id).values('major').first()
    user_college = find_user_college(user_major)

    data = get_user_GE_standard(student_year, user_college)

    table1 = []
    table2 = []
    table3 = []
    table4 = []
    my_list = []
    rest_list = []
    count = 0


    for i in MyDoneLecture.objects.filter(user_id=user_id):
        my_list = list(MyDoneLecture.objects.filter(user_id=user_id).values('year', 'semester', 'lecture_name', 'lecture_type','credit', 'lecture_topic', 'matched_topic'))

    #트리니티 이전
    if (int(student_year) < 2022):

        #####교필#####
        for item in data['essential_GE_standard']:
                for key, value in item.items():
                    if key != '총합':
                        table1.append({
                            "topic" : key,
                            "standard" : value,
                            "list" : []
                        })

        for item in my_list:
            if item['matched_topic'] in ['인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', 'MSC교과군', '철학적인간학', '신학적인간학']:
                for i in table1:
                    if i['topic'] == item['matched_topic']:
                        i['list'].append(item)

        #####교선#####
        for item in data['chocie_GE_standard']:
                for key, value in item.items():
                    if key != '총합':
                        table2.append({
                            "topic" : key,
                            "standard" : value,
                            "list" : []
                        })

        for item in my_list:
            if item['matched_topic'] in ['계열기초', '고전탐구', '사유와지혜', '가치와실천', '상상력과표현', '인문융합', '균형1', '균형2', '균형3', '균형4']:
                for i in table2:
                    if i['topic'] == item['matched_topic']:
                        i['list'].append(item)

        #####일반선택#####
        for item in my_list:
            if item['matched_topic'] == '' and item['lecture_type'] in ['교양', '교필', '교선']:
                count += item['credit']
                rest_list.append(item)

        table4 = {
            "topic" : "일선",
            "standard" : count,
            "list" : rest_list
        }
                    
    
    #트리니티 이후
    else:
        #####인성#####
        for item in data['humanism_GE_standard']:
                for key, value in item.items():
                    if key != '총합':
                        table1.append({
                            "topic" : key,
                            "standard" : value,
                            "list" : []
                        })

        for item in my_list:
            if item['matched_topic'] in ['인간학', '봉사활동', 'VERUM캠프', '트리니티아카데미']:
                for i in table1:
                    if i['topic'] == item['matched_topic']:
                        i['list'].append(item)

        #####기초#####
        for item in data['basic_GE_standard']:
                for key, value in item.items():
                    if key != '총합':
                        table2.append({
                            "topic" : key,
                            "standard" : value,
                            "list" : []
                        })

        for item in my_list:
            if item['matched_topic'] in ['소통', '논리적사고와글쓰기', '외국어', '자기관리', '진로탐색', '창의성', '창업', '계열기초', '디지털소통']:
                for i in table2:
                    if i['topic'] == item['matched_topic']:
                        i['list'].append(item)

        #####융합#####
        for item in data['fusion_GE_standard']:
                for key, value in item.items():
                    if key != '총합':
                        table3.append({
                            "topic" : key,
                            "standard" : value,
                            "list" : []
                        })

        for item in my_list:
            if item['matched_topic'] in ['정보활용', '창의융합', '문제해결', '융합비고']:
                for i in table3:
                    if i['topic'] == item['matched_topic']:
                        i['list'].append(item)


        #####일반선택#####
        for item in my_list:
            if item['matched_topic'] == '' and item['lecture_type'] in ['교양', '교필', '교선']:
                count += item['credit']
                rest_list.append(item)

        table4 = {
            "topic" : "일선",
            "standard" : count,
            "list" : rest_list
        }

    return table1, table2, table3, table4