from django.db.models import Count
from django.shortcuts import render
from app1.models import Product,ProductImages,Category

def index(request):
    products = Product.objects.filter(featured = True)
    latest = Product.objects.all().order_by("-id")[:10]
    categories =Category.objects.all()

    
    context = {
        "products":products,
        "latest":latest,
        "categories":categories
    }
    return render(request, 'app1/index.html',context)


def product_list(request):
    
    products = Product.objects.all()
    categories =Category.objects.all()
    
    context = {
        "products":products,
        "categories":categories
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


def product_detail(request,pid):
    product = Product.objects.get(pid = pid)
    p_image =product.p_images.all()
    category = Category.objects.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    
    
    context={
        "product":product,
        "p_image":p_image,
        "category":category,
        "products":products
        
        
        
    }
    return render (request,'app1/product_detail.html',context)
