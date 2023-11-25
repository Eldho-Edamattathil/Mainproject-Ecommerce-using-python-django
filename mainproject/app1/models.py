from django.db import models
from shortuuidfield import ShortUUIDField


from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICE = (
  ("process", "Processing"),
  ("shipped", "Shipped"),
  ("delivered", "Delivered")
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
  value = models.CharField(max_length=50,null =True,blank=True) 
  code = models.CharField(max_length=10, null=True, blank=True)
  
  def __str__(self):
      return self.value 
    
class Varients(models.Model):
  title =models.CharField(max_length=100,blank=True, null=True)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  size=models.ForeignKey(Size,on_delete=models.CASCADE,blank=True,null=True)
  image_id =models.IntegerField(default = 0,blank=True,null=True)
  stock_count =models.IntegerField (default=1)
  price =models.FloatField(default=0)
  old_price =models.FloatField(default =0)
  
  
  # def image(self):
  
  #   if self.image is not None:
  #     pass
      
  def image(self):
    img=ProductImages.objects.get(id =self.image_id)
    if img.id is not None:
      varimage = img.Images.url  
    else:
      varimage=''
    return varimage
      
      
  def varient_image(self):
    return mark_safe('<img src= "%s" width="50" height= "50" />' % (self.image.url)) 
    
    
  def __str__(self):
    return self.title
  

####################cart, Order, OrderItems, address################ 