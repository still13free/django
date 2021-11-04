from django.shortcuts import get_object_or_404, render
from basketapp.models import Basket

from mainapp.models import Product, ProductCategory
import random


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return None


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    return Product.objects.all().filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


def get_product_categories():
    return ProductCategory.objects.all()


def main(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4],
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', context=context)


def contacts(request):
    context = {
        'title': 'Контакты',
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/contacts.html', context=context)


def products(request, pk=None):
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0,
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.all().filter(category__pk=pk)
        context = {
            'title': 'Продукты',
            'links_menu': get_product_categories(),
            'category': category_item,
            'products': products_list,
            'basket': get_basket(request.user),
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'title': 'Продукты',
        'links_menu': get_product_categories(),
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
        'links_menu': get_product_categories(),
    }
    return render(request, 'mainapp/product.html', context)
