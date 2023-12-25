from django import forms

from app1.models import ProductReview,ProductOffer,CategoryOffer,Category
from stripe import Review
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError


class ProductReviewForm(forms.ModelForm):
  review= forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write Review"}))
  
  class Meta:
    model=ProductReview
    fields=['review','rating']
    
    
    
class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['discount_percentage', 'start_date', 'end_date', 'active']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data['discount_percentage']
        if not (0 <= discount_percentage <= 100):
            raise forms.ValidationError('Discount percentage must be between 0 and 100.')
        return discount_percentage
    def clean_active(self):
        active = self.cleaned_data['active']
        existing_product_offer = CategoryOffer.objects.filter(active=True).exists()

        if active and existing_product_offer:
            raise ValidationError('A Category offer is already active. Deactivate it before activating a Product offer.')

        return active


class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ['category', 'discount_percentage', 'start_date', 'end_date', 'active']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryOfferForm, self).__init__(*args, **kwargs)
        # Limit the choices for the 'category' field to available categories
        self.fields['category'].queryset = Category.objects.all()
        
        
    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data['discount_percentage']
        if not (0 <= discount_percentage <= 100):
            raise forms.ValidationError('Discount percentage must be between 0 and 100.')
        return discount_percentage
      
    def clean_active(self):
        active = self.cleaned_data['active']
        existing_product_offer = ProductOffer.objects.filter(active=True).exists()

        if active and existing_product_offer:
            raise ValidationError('A product offer is already active. Deactivate it before activating a category offer.')

        return active
