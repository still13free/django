from adminapp import views
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', views.user_create, name='user_create'),
    path('users/', views.users, name='user_list'),
    path('users/update/<int:pk>/', views.user_update, name='user_update'),
    path('users/status/<int:pk>/', views.user_status, name='user_status'),

    path('categories/create/', views.category_create, name='category_create'),
    path('categories/', views.categories, name='category_list'),
    path('categories/update/<int:pk>/',
         views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/',
         views.category_status, name='category_status'),

    path('products/create/category/<int:pk>/',
         views.product_create, name='product_create'),
    path('products/read/category/<int:pk>/',
         views.products, name='product_list'),
    path('products/detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/update/<int:pk>/', views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
]
