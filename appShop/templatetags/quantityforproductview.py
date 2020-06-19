from django import template
from appShop.models import OrderItem, Item

register = template.Library()

@register.simple_tag
def TheQuantity(*args, **kwargs):
    try:
        a= kwargs['U']
        b= kwargs['S']
        query = OrderItem.objects.get(user= a, ordered= False, item__slug= b)
        return query.quantity
    
    except:
        return 0
        

