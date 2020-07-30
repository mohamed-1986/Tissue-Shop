# Another way to show total receit and quantityPrice function in models
# is to make a simple tag for all
from django import template
from appShop.models import OrderItem

register = template.Library()

@register.simple_tag
def Totals(*args, **kwargs):
    a= kwargs['U']
    AllOrders= OrderItem.objects.filter(user= a, ordered= False).all()
    tot= 0
    for i in AllOrders:
        if i.item.discount_price:
            tot += i.quantity * i.item.discount_price
        else:
            tot += i.quantity * i.item.price
    return tot
