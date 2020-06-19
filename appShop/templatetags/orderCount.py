from django import template
from appShop.models import OrderItem

register = template.Library()

@register.filter
def counter(user):
    A= OrderItem.objects.filter(user= user, ordered= False).all()
    return A.count()


