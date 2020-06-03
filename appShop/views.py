from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order, CAT_CHOISES
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from appShop.forms import quant


def Checkout(request):
    if request.user.is_authenticated:
        qs= OrderItem.objects.filter(user= request.user, ordered= False).all()
        context= {'orderitem': qs}
        return render(request, 'appShop/checkout-page.html', context)
    else:
        return redirect("/")
    

class HomeView(ListView):
    model= Item
    template_name = "appShop/home.html"
    paginate_by = 8
    ordering= ["-date_added"]
  

def HomeViewFiltered(request, slug):
    qs= Item.objects.filter(category= slug).all()
    paginator = Paginator(qs, 8)
    page = request.GET.get('page')
    qsList = paginator.get_page(page)
    return render(request, 'appShop/homeCatFiltered.html',{'categs': qsList})

class ProductView(DetailView):
    model= Item
    template_name= "appShop/product.html"

# @login_required
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

    if Order_qs.exists():
        Order_first = Order_qs[0]
        if Order.objects.filter(items__item__slug= slug ).exists():
            order_item.quantity +=1
            order_item.save()
            messages.add_message(request, messages.INFO, 'Item quantity is modified.')
        else:
            Order_first.items.add(order_item)
            messages.add_message(request, messages.INFO, 'The item is added to cart')
    else:
        x= Order(user= request.user)
        x.orderedDate= timezone.now()
        x.save()
        x.items.add(order_item)
        messages.add_message(request, messages.INFO, 'New order has created')
        messages.add_message(request, messages.INFO, 'Item is added to cart')
    # b=OrderItem.objects.all().count()

    return redirect("appShop:productUrl", slug= slug)

def RemoveFromCart(request, slug):
    #loading Item, orderItem, Order:
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

def profile(request):
    return redirect("/")

def Info(request):
    return render(request, "appShop/Info.html")

def About(request):
    return render(request, "appShop/About.html")

def Contact(request):
    return render(request, "appShop/Contact.html")
