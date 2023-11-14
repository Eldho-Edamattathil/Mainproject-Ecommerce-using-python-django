from django.db.models import Count
from django.shortcuts import render
from app1.models import Product,ProductImages,Category

def index(request):
    products = Product.objects.filter(featured = True)
    latest = Product.objects.all().order_by("-id")[:10]

    
    context = {
        "products":products,
        "latest":latest
    }
    return render(request, 'app1/index.html',context)


def product_list(request):
    
    products = Product.objects.all()
    
    context = {
        "products":products
    }
    
    return render(request,'app1/product_list.html', context)


def category_list(request):
    category = Category.objects.all()
    
    
    context ={
        "category":category,
       
    }
    return render(request,'app1/category_list.html', context )



def category_product_list(request, cid):
    category = Category.objects.get(cid=cid)
    product = Product.objects.filter(category=category)
    
    
    context ={
        "category":category,
        "product":product
    }
    
    return render(request,'app1/category_product_list.html', context)
