from app1.models import Product,ProductImages,Category


def default(request):
  categories = Category.objects.filter(is_blocked =False)
  
  return {
    "categories":categories
  }