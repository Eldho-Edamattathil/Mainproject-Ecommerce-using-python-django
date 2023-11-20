from django import forms
from app1.models import Product
from django.core.exceptions import ValidationError

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




class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['Images']
