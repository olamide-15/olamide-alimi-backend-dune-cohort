from django.shortcuts import render,redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages

def home(request):
    return render(request, 'products/home.html')

def about(request):
    return render(request, 'products/about.html')

def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'products/product_list.html', {'products': products, 'query': query})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    for category in categories:
        category.product_count = Product.objects.filter(category=category).count()
    return render(request, 'products/category_list.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'category was added  sucessesfully')
            return redirect('category_list') 
    else:
        form = CategoryForm()
        return render(request, 'products/category_form.html', {'form': form})
    
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'category was updated sucessesfully')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
        return render (request,'products/category_form.html', {'form': form})
    
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method =='POST':
        category_name = category.name
        category.delete()

        messages.success(request, f'{category_name} deleted sucessfully.')
        return redirect('category_list')
    return render(request,'products/category_confirm_delete.html', {'category': category})
    

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'product was added  sucessesfully')
            return redirect('product_list') 
    else:
        form = ProductForm()
        return render(request, 'products/product_form.html', {'form': form})
    

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'product was updated sucessesfully')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        return render (request,'products/product_form.html', {'form': form})
    
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method =='POST':
        product_name = product.name
        product.delete()

        messages.success(request, f'{product_name} deleted sucessfully.')
        return redirect('product_list')
    return render(request,'products/product_confirm_delete.html', {'product': product})



# def custom_404(request, exception):
#     return render(request, 'products/home.html', status=404)
