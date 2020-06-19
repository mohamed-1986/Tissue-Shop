from django import forms

class QuantityForm(forms.Form):
    # a = forms.IntegerField()
    number= forms.ChoiceField(choices= [(x,x) for x in range (1,13)])

# from django.forms import ModelForm
# from appShop.models import OrderItem

# class AddToCartForm(ModelForm):
#     class Meta:
#         model= OrderItem
#         fields= ['quantity']