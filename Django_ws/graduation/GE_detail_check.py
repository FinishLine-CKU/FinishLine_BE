from user.models import User
from .GE_calculate import find_user_college
from .GE_calculate import get_user_GE_standard
from .models import MyDoneLecture
from .micro_degree_calculate import select_user_standard
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
    rest_count = 0
    success_count_1 = 0
    success_count_2 = 0
    success_count_3 = 0

    my_list = list(
        MyDoneLecture.objects.filter(user_id=user_id)
        .values('year', 'semester', 'lecture_name', 'lecture_type', 'credit', 'lecture_topic', 'matched_topic')
    )

    MD_standard, rest_standard = select_user_standard(user_id)

    if student_year in ['2018', '2019']:
        standard_order = ['철학적인간학', '신학적인간학', '인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', '고전탐구', '사유와지혜', '가치와실천', '상상력과표현', '인문융합', '균형1', '균형2', '균형3', '균형4']
    elif student_year in ['2020', '2021', '2022']:
        standard_order = ['인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', 'MSC교과군', '외국어', '계열기초', '사유와지혜', '가치와실천', '상상력과표현', '인문융합', '균형1', '균형2', '균형3', '균형4']
    elif student_year in ['2023', '2024', '2025']: 
        standard_order = ['VERUM캠프', '봉사활동', '트리니티아카데미', '인간학', '소통', '디지털소통', '자기관리', '정보활용', '창의융합', '문제해결']

    for item in my_list:
        item['year'] = item['year'][2:]

    #트리니티 이전
    if (int(student_year) < 2023):

        #####교필#####
        for ordered in standard_order:
            for item in data['essential_GE_standard']:
                if ordered in item:
                    table1.append({
                        "topic": ordered,
                        "standard": item[ordered],
                        "subject": []
                    })

        for item in my_list:
            if item['matched_topic'] in ['인간학', '봉사활동', 'VERUM캠프', '논리적사고와글쓰기', '창의적사고와코딩', '외국어', 'MSC교과군', '철학적인간학', '신학적인간학']:
                for i in table1:
                    if i['topic'] == item['matched_topic']:
                        i['subject'].append(item)
                        success_count_1 += item['credit']

        if success_count_1 >= data['essential_GE_standard'][0]['총합']:
            table1.append({
                "success" : 'true',
            })
        else:
            table1.append({
                "success" : 'false',
            })


        #####교선#####
        for ordered in standard_order:
            for item in data['chocie_GE_standard']:
                if ordered in item:
                    table2.append({
                        "topic": ordered,
                        "standard": item[ordered],
                        "subject": []
                    })

        for item in my_list:
            if item['matched_topic'] in ['계열기초', '고전탐구', '사유와지혜', '가치와실천', '상상력과표현', '인문융합', '균형1', '균형2', '균형3', '균형4']:
                for i in table2:
                    if i['topic'] == item['matched_topic']:
                        i['subject'].append(item)
                        success_count_2 += item['credit']

        if success_count_2 >= data['chocie_GE_standard'][0]['총합']:
            table2.append({
                "success" : 'true',
            })
        else:
            table2.append({
                "success" : 'false',
            })

        #####일반선택#####
        for item in my_list:
            if item['matched_topic'] == '일반선택':
                rest_list.append(item)

        table4 = {
            "topic" : "일반선택",
            "standard" : rest_standard,
            "subject" : rest_list
        }
                    
    
    #트리니티 이후
    else:

        #####인성#####
        for ordered in standard_order:
            for item in data['humanism_GE_standard']:
                if ordered in item:
                    table1.append({
                        "topic": ordered,
                        "standard": item[ordered],
                        "subject": []
                    })

        for item in my_list:
            if item['matched_topic'] in ['인간학', '봉사활동', 'VERUM캠프', '트리니티아카데미']:
                for i in table1:
                    if i['topic'] == item['matched_topic']:
                        i['subject'].append(item)
                        success_count_1 += item['credit']

        if success_count_1 >= data['humanism_GE_standard'][0]['총합']:
            table1.append({
                "success" : 'true',
            })
        else:
            table1.append({
                "success" : 'false',
            })

        #####기초#####
        for ordered in standard_order:
            for item in data['basic_GE_standard']:
                if ordered in item:
                    table2.append({
                        "topic": ordered,
                        "standard": item[ordered],
                        "subject": []
                    })

        for item in my_list:
            if item['matched_topic'] in ['소통', '논리적사고와글쓰기', '외국어', '자기관리', '진로탐색', '창의성', '창업', '계열기초', '디지털소통']:
                for i in table2:
                    if i['topic'] == item['matched_topic']:
                        i['subject'].append(item)
                        success_count_2 += item['credit']

        if success_count_2 >= data['basic_GE_standard'][0]['총합']:
            table2.append({
                "success" : 'true',
            })
        else:
            table2.append({
                "success" : 'false',
            })

        #####융합#####
        for ordered in standard_order:
            for item in data['fusion_GE_standard']:
                if ordered in item:
                    table3.append({
                        "topic": ordered,
                        "standard": item[ordered],
                        "subject": []
                    })

        for item in my_list:
            if item['matched_topic'] in ['정보활용', '창의융합', '문제해결', '융합비고']:
                for i in table3:
                    if i['topic'] == item['matched_topic']:
                        i['subject'].append(item)
                        success_count_3 += item['credit']

        if success_count_3 >= data['fusion_GE_standard'][0]['총합']:
            table3.append({
                "success" : 'true',
            })
        else:
            table3.append({
                "success" : 'false',
            })


        #####일반선택#####
        for item in my_list:
            if item['matched_topic'] == '일반선택':
                rest_list.append(item)

        table4 = {
            "topic" : "일반선택",
            "standard" : rest_standard,
            "subject" : rest_list
        }

    return table1, table2, table3, table4