from django.contrib import admin
from django.conf import settings
# Register your models here.
from django.contrib.auth import get_user_model
from app1.models import Product, Category, ProductImages,Size,Varients


admin.site.register(get_user_model())

class ProductImagesAdmin(admin.TabularInline):
  model = ProductImages
  
class ProductVarientsAdmin(admin.TabularInline):
  model = Varients
  

  
class ProductAdmin(admin.ModelAdmin):
  inlines = [ProductImagesAdmin,ProductVarientsAdmin]
  list_display = ['title','product_image','price','category','featured','status','pid','varient']
  
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['title', 'category_image']
  
class SizeAdmin(admin.ModelAdmin):
  list_display = ['value', 'code']
  
class VarientAdmin(admin.ModelAdmin):
  list_display = ['title', 'product','size','image_id','stock_count','price','old_price']






admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Varients,VarientAdmin)



