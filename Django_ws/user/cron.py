from user.models import VisitorCount

def reset_today_visitor_count():

    visitor = VisitorCount.objects.filter(id=1).first()
    visitor.total_visitor = 1
    visitor.save()
