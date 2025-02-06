from .models import Standard

standard1 = Standard.objects.create(
    college="일반대학",
    year="2018",
    total_credit=130.0,
    major_credit=69.0,
    general_essential_credit=16.0,
    general_selection_credit=20.0,
    rest_credit=25.0,
)

standard1.save()

print(standard1)