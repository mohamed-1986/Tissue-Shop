from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (HomeView, ProductView, AddToCart, 
           Checkout, Profile, RemoveFromCart,
           HomeViewFiltered, 
           Info, Contact, About,
           Cart,
           )

app_name= 'appShop'

urlpatterns = [
    path('', HomeView.as_view(), name='homeUrl'),
    path('category/<slug>/', HomeViewFiltered, name='HomeCategoryUrl'),
    path('accounts/signup/next/', Profile),
    path('product/<slug>/',  ProductView.as_view(), name='productUrl'),
    path('add-to-cart/<slug>/', AddToCart , name='addToCartUrl'),
    path('remove-from-cart/<slug>/', RemoveFromCart , name='removeFromCartUrl'),
    # path('removeFromCart/',RemoveFromCart , name='removeFromCartUrl' ) ,
    path('checkout/', Checkout ,name= 'checkoutUrl'),
    path('info/', Info, name='infoUrl'),
    path('contact/', Contact, name='contactUrl'),
    path('about/',About , name='aboutUrl'),
    path('cart/', Cart, name='cartUrl'),
]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)