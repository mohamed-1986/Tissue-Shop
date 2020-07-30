from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order, CAT_CHOISES
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import QuantityForm



def Checkout(request):
    if request.user.is_authenticated:
        qs= OrderItem.objects.filter(user= request.user, ordered= False).all()
        context= {'orderitem': qs}
        return render(request, 'appShop/checkout-page.html', context)
    else:
        messages.add_message(request, messages.INFO, "لم تقم بتسجيل الدخول")
        return redirect("/")
    

class HomeView(ListView):
    model= Item
    template_name = "appShop/home.html"
    paginate_by = 2
    ordering= ["-date_added"]
  

def HomeViewFiltered(request, slug):
    qs= Item.objects.filter(category= slug).all()
    paginator = Paginator(qs, 8)
    page = request.GET.get('page')
    qsList = paginator.get_page(page)
    return render(request, 'appShop/homeCatFiltered.html',{'categs': qsList})

class ProductView(DetailView):
    model= Item
    template_name = "appShop/product.html"
    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['form'] = QuantityForm() 
        return context
    

# @login_required(login_url='/accounts/login/')
# def AddToCart(request, slug):
#     #loading Item, orderItem, Order:
#     item= get_object_or_404(Item, slug= slug)
#     order_item, created= OrderItem.objects.get_or_create(
#         item= item,
#         user= request.user,
#         ordered= False
#         )
#     Order_qs= Order.objects.filter(
#         user= request.user,
#         ordered= False
#     )

#     if Order_qs.exists():
#         Order_first = Order_qs[0]
#         if Order.objects.filter(items__item__slug= slug ).exists():
#             order_item.quantity +=1
#             order_item.save()
#             messages.add_message(request, messages.INFO, 'Item quantity is modified.')
#         else:
#             Order_first.items.add(order_item)
#             messages.add_message(request, messages.INFO, 'The item is added to cart')
#     else:
#         x= Order(user= request.user)
#         x.orderedDate= timezone.now()
#         x.save()
#         x.items.add(order_item)
#         messages.add_message(request, messages.INFO, 'New order has created')
#         messages.add_message(request, messages.INFO, 'Item is added to cart')
#     # b=OrderItem.objects.all().count()

#     return redirect("appShop:productUrl", slug= slug)

@login_required(login_url='/accounts/login/')
def AddToCart(request, slug):
    #loading Item, orderItem, Order:
    item= get_object_or_404(Item, slug= slug)
    order_item, created= OrderItem.objects.get_or_create(
        item= item,
        user= request.user,
        ordered= False
        )
    Order_qs= Order.objects.filter(
        user= request.user,
        ordered= False
    )
    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
        I= QuantityForm(request.POST)
        
# check whether it's valid:
        if I.is_valid():
            num= I.cleaned_data['number']
            #check if current user has an active order?!
            if Order_qs.exists():
                Order_first = Order_qs[0]
                #check if that order contains the item required?!
                if Order.objects.filter(items__item__slug= slug ).exists():
                    print(order_item.quantity)
                    order_item.quantity = order_item.quantity+ int(num)
                    order_item.save()
                    messages.add_message(request, messages.INFO, 'Item quantity is modified.')
                #here we are sure that the user ahs an active order but not containing the 
                #specific item
                else:
                    order_item.quantity = num
                    order_item.save()
                    Order_first.items.add(order_item)
                    messages.add_message(request, messages.INFO, 'The item is added to cart')
            else:
                x= Order(user= request.user)
                x.orderedDate= timezone.now()
                x.save()
                order_item.quantity = num
                x.items.add(order_item)
                messages.add_message(request, messages.INFO, 'New order has created')
                messages.add_message(request, messages.INFO, 'Item is added to cart')
    
    return redirect("appShop:productUrl", slug= slug)

@login_required(login_url='/accounts/login/')
def RemoveFromCart(request,slug):
    try:
        item= Item.objects.get(slug= slug)
        order_item = OrderItem.objects.get(
            item= item,
            user= request.user,
            ordered= False
            )
        order_item.delete()
        messages.add_message(request, messages.INFO, 'Item has deleted')
    except:
        messages.add_message(request, messages.INFO, 'Item is not found')

    return redirect("appShop:productUrl", slug= slug)

def Profile(request):
    return redirect("/")

def Info(request):
    return render(request, "appShop/Info.html")

def About(request):
    return render(request, "appShop/About.html")

def Contact(request):
    return render(request, "appShop/Contact.html")

@login_required(login_url='/accounts/login/')
def Cart(request):
    
    myOrderItems= OrderItem.objects.filter(
        user= request.user,
        ordered= False )
    total=0
    
    if myOrderItems:
        for i in myOrderItems:
            if i.item.discount_price:
                total += i.quantity* i.item.discount_price
            else:
                total += i.quantity * i.item.price
        context= {
            "myOrderItems": myOrderItems }
            # "total": 10}
        return render(request, "appShop/cart.html", context)
    else:
        messages.add_message(request, messages.INFO, 'سلة الشراء فارغة')
        return redirect("/")