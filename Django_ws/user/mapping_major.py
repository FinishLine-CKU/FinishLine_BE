from user.models import MajorMap
from user.models import MajorAlias

def mapping_major(major):
    if MajorAlias.objects.filter(alias = major).exists():
        major_code = MajorAlias.objects.filter(alias = major).first().major_code
        user_major = MajorMap.objects.filter(major_code = major_code).first()
        major_label = user_major.major_label
        college = user_major.college
        return major_label, college
    else:
        errorMessage = '회원 정보를 확인할 수 없습니다. 잠시 후 다시 시도해주세요.'
        return errorMessage