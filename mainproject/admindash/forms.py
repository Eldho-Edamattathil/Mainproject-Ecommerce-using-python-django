from django import forms
from app1.models import Product,CartOrder,Coupon
from django.core.exceptions import ValidationError
from decimal import Decimal



from app1.models import ProductImages

class CreateProductForm(forms.ModelForm):
    new_image = forms.ImageField(required=False)  # Add this line for the new image field
    
    class Meta:
        model = Product
        fields = ['title', 'category', 'old_price', 'price', 'description', 'stock_count', 'new_image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
    def clean_stock_count(self):
        stock_count = self.cleaned_data.get('stock_count')

        if stock_count is not None and stock_count < '0':
            raise ValidationError("Stock count cannot be negative.")

        return stock_count
    
    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price < Decimal('0'):
            raise ValidationError("Price cannot be negative.")

        return price
    
    def clean_old_price(self):
        old_price = self.cleaned_data.get('old_price')

        if old_price is not None and old_price < Decimal('0'):
            raise ValidationError("Price cannot be negative.")

        return old_price




class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['Images']
        
        
class CouponForm(forms.Form):
    code = forms.CharField(max_length=50)
    
    
# class CouponForm(forms.ModelForm):
#     class Meta:
#         model = Coupon
#         fields = ['code', 'discount', 'active', 'active_date', 'expiry_date']
#         widgets = {
#             'active_date': forms.DateInput(attrs={'type': 'date'}),
#             'expiry_date': forms.DateInput(attrs={'type': 'date'}),
#             'discount': forms.NumberInput(attrs={'min': '0', 'max': '100'}),
#             'active': forms.CheckboxInput(),
#         }
        
        
        
