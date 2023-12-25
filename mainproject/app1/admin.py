from django.contrib import admin
from django.conf import settings
# Register your models here.
from django.contrib.auth import get_user_model
from app1.models import Product, Category, ProductImages,Size,Variants,CartOrderItems,CartOrder,Address,UserDetails,Coupon,wishlist_model,wallet,ProductReview,ProductOffer,CategoryOffer
# from userauths.models import profile


admin.site.register(get_user_model())

class ProductImagesAdmin(admin.TabularInline):
  model = ProductImages
  
class ProductVarientsAdmin(admin.TabularInline):
  model = Variants
  

  
class ProductAdmin(admin.ModelAdmin):
  inlines = [ProductImagesAdmin,ProductVarientsAdmin]
  list_display = ['title','product_image','price','category','featured','status','pid','varient']
  
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['title', 'category_image']
  
class SizeAdmin(admin.ModelAdmin):
  list_display = ['value', 'code']
  
class VariantAdmin(admin.ModelAdmin):
  list_display = ['title', 'product','size','image_id','stock_count','price','old_price']
  
  
class CartOrderAdmin(admin.ModelAdmin):
  list_editable=['paid_status','product_status']
  list_display=['user','price','paid_status','order_date','product_status']
  
class CartOrderItemsAdmin(admin.ModelAdmin):
  list_display=['order','invoice_no','item','image','qty','price','total']
  
  
class AddressAdmin(admin.ModelAdmin):
  list_editable=['address','status']
  list_display=['user','address','status']




class UserDetailsAdmin(admin.ModelAdmin):
  list_display=['full_name','bio','phone']


class CouponAdmin(admin.ModelAdmin):
  list_display=['code','discount','active','active_date','expiry_date','created_date']
  
  
class WishlistAdmin(admin.ModelAdmin):
  list_display=['user','product','Date']
  
  
  
class walletAdmin(admin.ModelAdmin):
  list_display=['user','Amount']

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderItemsAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(UserDetails,UserDetailsAdmin)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(wishlist_model,WishlistAdmin)
admin.site.register(wallet,walletAdmin)
admin.site.register(ProductReview)
admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)




