from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView, CategoryListAPIView, CategoryDetailAPIView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('about/', views.about, name='about'),

    path('products/add/', views.product_create, name= 'product_create'),
    path('products/<int:pk>/edit/', views.product_update, name= 'product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name= 'product_delete'),

    path('categories/add/', views.category_create, name= 'category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name= 'category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name= 'category_delete'),

    path('api/products/', ProductListAPIView.as_view(), name='api_product_list'),
    path('api/products/<int:pk>/', ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('api/categories/', CategoryListAPIView.as_view(), name='api_category_list'),   
    path('api/categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='api_category_detail'),
]

