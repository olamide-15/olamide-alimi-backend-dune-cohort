from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    return render(request, 'products/home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    for category in categories:
        category.product_count = Product.objects.filter(category=category).count()
    return render(request, 'products/category_list.html', {'categories': categories})

def about(request):
    return render(request, 'products/home.html')

def custom_404(request, exception):
    return render(request, 'products/home.html', status=404)
