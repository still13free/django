from django.urls import path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.products, name='products'),
    path('category/<int:pk>/', views.products, name='category'),
    path('category/<int:pk>/<page>/', views.products, name='category_page'),
    path('product/<int:pk>/', views.product, name='product'),
]
