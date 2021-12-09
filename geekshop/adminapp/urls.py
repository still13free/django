from adminapp import views
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', views.user_create, name='user_create'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/update/<int:pk>/', views.user_update, name='user_update'),
    path('users/status/<int:pk>/', views.user_status, name='user_status'),

    path('categories/create/', views.category_create, name='category_create'),
    path('categories/', views.categories, name='category_list'),
    path('categories/update/<int:pk>/',
         views.category_update, name='category_update'),
    path('categories/status/<int:pk>/',
         views.category_status, name='category_status'),

    path('products/create/category/<int:pk>/',
         views.ProductCreateView.as_view(), name='product_create'),
    path('products/read/category/<int:pk>/',
         views.ProductsListView.as_view(), name='product_list'),
    path('products/detail/<int:pk>/',
         views.ProductDetailView.as_view(), name='product_detail'),
    path('products/update/<int:pk>/',
         views.ProductUpdateView.as_view(), name='product_update'),
    path('products/status/<int:pk>/',
         views.ProductDeleteView.as_view(), name='product_status'),
]
