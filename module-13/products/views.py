from django.contrib.auth.decorators import login_required 
from django.shortcuts import render,redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializers, CategorySerializers

def home(request):
    return render(request, 'products/home.html')

def about(request):
    return render(request, 'products/about.html')

def product_list(request):
    query = request.GET.get('product-name', '')
    
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products, 'product_name': query})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    for category in categories:
        category.product_count = Product.objects.filter(category=category).count()
    return render(request, 'products/category_list.html', {'categories': categories})

@login_required
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

@login_required  
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
    
@login_required   
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method =='POST':
        category_name = category.name
        category.delete()

        messages.success(request, f'{category_name} deleted sucessfully.')
        return redirect('category_list')
    return render(request,'products/category_confirm_delete.html', {'category': category})
    
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            messages.success(request, 'product was added  sucessesfully')
            return redirect('product_list') 
    else:
        form = ProductForm()
        return render(request, 'products/product_form.html', {'form': form})
    
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'product was updated sucessesfully')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        return render (request,'products/product_form.html', {'form': form})

@login_required   
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Resrict to staff
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to delete this product.")
        return redirect('product_list')
    
    if request.method =='POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'{product_name} deleted sucessfully.')
        return redirect('product_list')
    return render(request,'products/product_confirm_delete.html', {'product': product})

def product_list_json(request):
    products = Product.objects.all()
    data = [{'id': p.id, 
             'name': p.name, 
             'price': str(p.price), 
             'stock': p.stock
             }
            for p in products]
   
    return JsonResponse(data, safe=False)

def product_detail_json(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        data = {'id': product.id, 
                'name': product.name, 
                'price': str(product.price)}
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
def category_list_json(request):
    categories = Category.objects.all()
    data = [{'id': c.id, 'name': c.name} for c in categories]
    return JsonResponse(data, safe=False)

def category_detail_json(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        data = {'id': category.id, 'name': category.name}
        return JsonResponse(data)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    
class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None
    
    def delete(self, request, pk):
        product = self.delete_object(pk)
        if product is None:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        
class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializers(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializers(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializers(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# def custom_404(request, exception):
#     return render(request, 'products/home.html', status=404)
