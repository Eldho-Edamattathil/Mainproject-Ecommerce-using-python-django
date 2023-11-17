from app1.models import Product,ProductImages,Category


def default(request):
  categories = Category.objects.all()
  
  return {
    "categories":categories
  }