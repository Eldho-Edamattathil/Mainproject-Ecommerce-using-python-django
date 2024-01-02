from django.db import models
from shortuuidfield import ShortUUIDField
from django.conf import settings
from django.shortcuts import reverse
from decimal import Decimal
from .utils import generate_ref_code


from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICE = (
  ("processing", "Processing"),
  ("shipped", "Shipped"),
  ("delivered", "Delivered"),
  ("cancelled","cancelled"),
) 

RATING = (
  (1,"⭐☆☆☆☆"),
  (2,"⭐⭐☆☆☆"),
  (3,"⭐⭐⭐☆☆"),
  (4,"⭐⭐⭐⭐☆"),
  (5,"⭐⭐⭐⭐⭐")
)
  


# def user_directory_path(instance,filename):
#   return 'user_{0}/{1}'.format(instance.user.id, filename)
def user_directory_path(instance, filename):
    if instance.user and instance.user.id:
        return 'user_{0}/{1}'.format(instance.user.id, filename)
    else:
        # Handle the case when user or user.id is None
        return 'user_unknown/{0}'.format(filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=20)
    title = models.CharField(max_length=100, default="Autoparts")
    image = models.ImageField(upload_to='category', default="category.jpg")
    is_blocked =models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title
    

class Tags(models.Model):
  pass

    

    
    
class Product(models.Model):
  
  Varients =(
    ('None','None'),
    ('Size','Size')
  )
  
  
  
  pid = ShortUUIDField(unique =True, max_length = 20)
  user = models.ForeignKey(User, on_delete = models.SET_NULL,null =True)
  category = models.ForeignKey(Category, on_delete = models.SET_NULL,null = True, related_name ="category")
  
  title = models.CharField(max_length = 100,default = "Fresh pear")
  image = models.ImageField(upload_to=user_directory_path, default = "product.jpg", null=True,blank=True)
  description = models.TextField(null =True, blank =True, default = "This is the product")
  
  price = models.DecimalField(max_digits =10, decimal_places =2, default = 1.99 )
  old_price = models.DecimalField(max_digits =10, decimal_places =2, default = 2.99)

  specifications = models.TextField(null =True, blank =True)
  type = models.CharField(max_length = 100,default = "Automobile",null=True, blank=True)
  stock_count = models.CharField(max_length = 100,default = "10",null=True, blank=True)
  mfd=models.DateTimeField(auto_now_add=False,null=True, blank=True)
  return_policy= models.CharField(max_length = 100,default = "10", null=True, blank=True)
  warrenty = models.CharField(max_length = 100,default = "1", null=True, blank=True)
  varient=models.CharField(max_length=20,choices=Varients,default='None')
  
  
  
  
  # tags = models.ForeignKey(Tags, on_delete = models.SET_NULL, null =True)
  
  
  
  status = models.BooleanField(default=True)
  in_stock = models.BooleanField(default=True)
  featured = models.BooleanField(default=False)
  digital = models.BooleanField(default=False)
  cod =models.BooleanField(default=True)  

    
  sku = ShortUUIDField(unique =True,max_length = 20)
  date = models.DateTimeField(auto_now_add =True)
  updated = models.DateTimeField(null=True, blank=True)

  class Meta:
    verbose_name_plural = "Products"
    
  def product_image(self):
    return mark_safe('<img src= "%s" width="50" height= "50" />' % (self.image.url))
  
  def __str__(self):
      return self.title
    
  def get_percentage(self):
    new_price = (self.price /self.old_price) * 100
    return new_price
    

class ProductImages(models.Model):
  Images = models.ImageField(upload_to="products-images", default = "product.jpg")
  product = models.ForeignKey(Product, related_name='p_images',on_delete = models.SET_NULL,null =True)
  date = models.DateField(auto_now_add =True)
  
  class Meta:
    verbose_name_plural = "Product Images"
    
    
class Size(models.Model):
  # sid = models.AutoField(primary_key=True)
  value = models.CharField(max_length=50,null =True,blank=True, default ='None') 
  code = models.CharField(max_length=10, null=True, blank=True)
  
  def __str__(self):
      return self.value 
    
class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.ForeignKey(ProductImages,on_delete=models.CASCADE, blank=True, null=True)
    stock_count = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    old_price = models.FloatField(default=0)

    def image(self):
        img = ProductImages.objects.filter(variant=self).first()
        return img.Images.url if img else ''

    def variant_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image())

    def __str__(self):
        return self.title
  

####################cart, Order, OrderItems, address################ 



# cart
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('cart_detail')  # Change 'cart_detail' to the URL name of your cart detail view

    def __str__(self):
        return f"Cart for {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in {self.cart.user.email}"
      
    def save(self, *args, **kwargs):
        self.total_price = float(self.product.price) * self.quantity
        super().save(*args, **kwargs)
        
        
        
class CartOrder(models.Model):
  user =models.ForeignKey(User, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=10,decimal_places=1,default = 1.99)
  paid_status=models.BooleanField(default=False)
  order_date=models.DateTimeField(auto_now_add=True)
  product_status=models.CharField(choices=STATUS_CHOICE,max_length=30,default="processing")
  wallet_status=models.BooleanField(default=False)
  
  
  class Meta:
    verbose_name_plural= "Cart order"
    
  def __str__(self):
        return f"Cart for {self.user.email}"
    
    
class CartOrderItems(models.Model):
  order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
  invoice_no=models.CharField(max_length=200)
  product_status=models.CharField(max_length=200)
  item = models.CharField(max_length=200)
  image =models.CharField(max_length=200)
  qty=models.IntegerField(default=0)
  price =models.DecimalField(max_digits=10,decimal_places=2,default=1.99)
  total =models.DecimalField(max_digits=10,decimal_places=2,default=1.99)
  
  
  
  class meta:
    verbose_name_plural ="Cart Order Items"
    
    
  def order_img(self):
    return mark_safe('<img src= "/media/%s" width="50" height= "50" />' % (self.image))
  
  
  
  
# Adresss

class Address(models.Model):
  user = models.ForeignKey(User,on_delete=models.SET_NULL, null =True)
  address = models.CharField(max_length=100,null=True)
  mobile = models.CharField(max_length=15,null=True)
  status = models.BooleanField(default=False)
  
  
  class meta:
    verbose_name_plural ="Address"
    
    
    
class UserDetails(models.Model):
  user=models.OneToOneField(User, on_delete=models.CASCADE)
  image=models.ImageField(upload_to='userimage')
  full_name=models.CharField(max_length=200, null=True,blank=True)
  bio = models.CharField(max_length=200, null=True, blank=True)
  phone =models.CharField(max_length=15, null=True,blank=True)
  verified =models.BooleanField(default=False)
  code=models.CharField(max_length=12, blank=True, null=True)
  recommended_by=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null =True,related_name='recommended_userdetails')
  updated=models.DateTimeField(auto_now=True)
  created=models.DateTimeField(auto_now=True)
  
  def __str__(self):
      return f"{self.user.username}---{self.code}"
    
  def get_recommend_profiles(self):
    pass
  
  def save(self, *args, **kwargs):
        if self.code is None:
            self.code = generate_ref_code()

        super().save(*args, **kwargs)
  
  
    
    
class Coupon(models.Model):
  code=models.CharField(max_length=50,unique=True)
  discount=models.PositiveIntegerField(help_text='discount in percentage')
  active=models.BooleanField(default=True)
  active_date=models.DateField()
  expiry_date=models.DateField()
  created_date=models.DateTimeField(auto_now_add=True)
  limit=models.PositiveIntegerField(null=True, blank=True)
  
  
  def __str__(self):
     return self.code
   
   
   
class wishlist_model(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  Date=models.DateTimeField(auto_now_add=True)
  
  
  
  class Meta:
    verbose_name_plural="Wishlists"
    
    
class wallet(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  Amount =models.DecimalField(max_digits=10,decimal_places=2,default=1.99)
  referral=models.BooleanField(default = False)
  
  class Meta:
    verbose_name_plural="Wallet"
    
  def __str__(self):
    return self.user.email 
  
  
  
class ProductReview(models.Model):
  user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
  product=models.ForeignKey(Product,on_delete=models.SET_NULL, null=True, related_name='reviews')
  review=models.TextField()
  rating=models.IntegerField(choices=RATING, default=None)
  date=models.DateTimeField(auto_now_add=True)
  
  
  class Meta:
    verbose_name_plural ='Product Reviews'
    
    
  def __str__(self):
    return self.product.title
  
  def get_rating(self):
    return self.rating
  
  
class ProductOffer(models.Model):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.discount_percentage}% Discount"

    def save(self, *args, **kwargs):
        # Ensure discount_percentage is Decimal type
        if not isinstance(self.discount_percentage, Decimal):
            self.discount_percentage = Decimal(str(self.discount_percentage))
        super().save(*args, **kwargs)
    
class CategoryOffer(models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.discount_percentage}% Discount"

    def save(self, *args, **kwargs):
        # Ensure discount_percentage is Decimal type
        if not isinstance(self.discount_percentage, Decimal):
            self.discount_percentage = Decimal(str(self.discount_percentage))
        super().save(*args, **kwargs)
        
        
