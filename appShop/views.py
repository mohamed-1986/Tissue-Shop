from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order, CAT_CHOISES, Billing
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import QuantityForm
from .models import BillForm
from django.core.mail import EmailMessage

@login_required(login_url='/accounts/login/')
def Checkout(request):
    try:
        OrderItem_qs = OrderItem.objects.filter(
            user= request.user ,
            ordered = False
            ).all()

        Order_qs = Order.objects.get(
            ordered = False , 
            user = request.user
            )
        
    except:
        OrderItem_qs = None
        Order_qs = None
    try:
        billing_qs = Billing.objects.get(user= request.user)
    except:
        billing_qs = None

    # IF user previously recorded billing address
    if request.method == 'POST':
        form = BillForm(request.POST , instance= billing_qs)
        if form.is_valid():
            F = form.save(commit= False)
            F.user = request.user
            F.save()
            # here we send E-mail with orderitems to merchant:
            contacts = ['mohamed.samir.saleh@gmail.com']
            body = list(OrderItem_qs)
            subject = "new order request"
            print("Contacts "   , contacts, " Body ", body , " Subject ", subject)
            email = EmailMessage(subject , body, to = contacts)
            email.send()
            # SendEmailNewOrder(subject, body, contacts)

            #turn the ordered into True in Oder , OrderItem:
            Order_qs.ordered = True
            Order_qs.save()
            elements = Order_qs.items.all()
            print(elements)
            for Element in elements:
                Element.ordered = True
                Element.save()


        print("order is ", OrderItem_qs)
        return HttpResponseRedirect('/')
   
    else:
        form = BillForm(initial={'user': request.user}, instance= billing_qs)
        return render(request, 'appShop/checkout.html', {'form': form})  


# def SendEmailNewOrder(subject, body, contacts):
#     email = EmailMessage(subject , body, to = contacts)
#     email.send()

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


@login_required(login_url='/accounts/login/')
def AddToCart(request, slug):
    #loading Item, orderItem, Order:
    item= get_object_or_404(Item, slug= slug)
    Order_qs= Order.objects.filter(
        user= request.user,
        ordered= False
    )
    order_item, created= OrderItem.objects.get_or_create(
        item= item,
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
                    order_item.quantity = order_item.quantity+ int(num)
                    order_item.save()
                    messages.add_message(request, messages.INFO, 'تم تعديل الكمية')
                #here we are sure that the user ahs an active order but not containing the 
                #specific item
                else:
                    order_item.quantity = num
                    order_item.save()
                    Order_first.items.add(order_item)
                    messages.add_message(request, messages.INFO, 'تم اضافة الصنف في السلة')
            else:
                x= Order(user= request.user)
                x.orderedDate= timezone.now()
                x.save()
                order_item.quantity = num
                order_item.save()
                x.items.add(order_item)
                x.save()
                messages.add_message(request, messages.INFO, 'تم اضافة طلب جديد و تم اضافة صنف في السلة')   
    return redirect("appShop:productUrl", slug= slug)

@login_required(login_url='/accounts/login/')
def RemoveFromCart(request):
    UrlGet = request.GET["nexturl"]
    SlugGet = request.GET["slug"]
    
    try:
        item= Item.objects.get(slug= SlugGet)
        order_item = OrderItem.objects.get(
            item= item,
            user= request.user,
            ordered= False
            )
        order_qs = Order.objects.get(
            user = request.user,
            ordered = False,
            items__item__slug = SlugGet
        )
        # order_qs.items.remove( order_item )
        # order_qs.save()
        order_item.delete()

        messages.add_message(request, messages.INFO, 'تم ازالة المنتج')
        order_qs = Order.objects.get(
            user = request.user,
            ordered = False
        )
        NoOfRemainingOrderItems= order_qs.items.all()
        print(NoOfRemainingOrderItems)
        if not NoOfRemainingOrderItems:
            print("there is no order items remained we have to delete the order")
            order_qs.delete()
            # order_qs.save()

    except:
        messages.add_message(request, messages.INFO, 'منتج غير موجود')
    return redirect(UrlGet)
    # return redirect("appShop:productUrl", slug= SlugGet)


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
        return render(request, "appShop/cart.html", context)
    else:
        messages.add_message(request, messages.INFO, 'سلة الشراء فارغة')
        return redirect("/")