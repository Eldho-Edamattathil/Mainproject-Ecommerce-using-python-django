from django import forms

from app1.models import ProductReview
from stripe import Review

class ProductReviewForm(forms.ModelForm):
  review= forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write Review"}))
  
  class Meta:
    model=ProductReview
    fields=['review','rating']
    
    


