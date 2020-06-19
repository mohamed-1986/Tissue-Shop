from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


CAT_CHOISES=(
    ('T', 'مناديل'),
    ('P', 'بلاستيك'),
    ('B', 'شنط'),
    ('M', 'حفاضات')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null =True, blank= True)
    category = models.CharField(choices= CAT_CHOISES, max_length= 1, default= 'T')
    slug = models.SlugField()
    description = models.TextField(max_length= 100, null =True, blank= True)
    image = models.ImageField(null =True, blank= True)
    date_added = models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('appShop:productUrl', kwargs={
            'slug': self.slug
        })

        # from django.urls import reverse
        # return reverse('appShop:productUrl',  args=[self.slug])
    
    # def get_cat_url(self):
    #     return reverse('appShop:HomeCategoryUrl', kwargs={
    #         'slug': self.category
    #     })


    def get_add_to_cart_url(self):
        return reverse('appShop:addToCartUrl', kwargs={
            'slug': self.slug
        })

    def remove_from_cart_url(self):
        return reverse('appShop:removeFromCartUrl', kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    item = models.ForeignKey(Item, on_delete= models.CASCADE)
    quantity = models.IntegerField(default= 1)
    ordered = models.BooleanField(default= False)

    def __str__(self):
        return (str(self.quantity)+ '  from the product: '+ self.item.title)
    
    def quantityPrice(self):
        return self.quantity* self.item.price
        
    def quantityDiscountPrice(self):
        return self.quantity* self.item.discount_price
    
class Order(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    items= models.ManyToManyField(OrderItem)
    startDate= models.DateTimeField(auto_now_add= True)
    orderedDate= models.DateTimeField()
    ordered= models.BooleanField(default= False)

    def __str__(self):
        return self.user.username
        # return str(self.orderedDate)