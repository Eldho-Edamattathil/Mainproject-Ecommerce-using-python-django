from django.contrib import admin
from django.conf import settings
# Register your models here.
from django.contrib.auth import get_user_model
from app1.models import Product, Category, ProductImages

admin.site.register(get_user_model())

class ProductImagesAdmin(admin.TabularInline):
  model = ProductImages
  
class ProductAdmin(admin.ModelAdmin):
  inlines = [ProductImagesAdmin]
  list_display = ['user','title','product_image','price','category','featured','status']
  
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['title', 'category_image']
  







admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)


