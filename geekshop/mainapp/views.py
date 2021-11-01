from django.shortcuts import get_object_or_404, render
from basketapp.models import Basket
from basketapp.views import basket

from mainapp.models import Product, ProductCategory
import random


def get_basket(user):
    if user.is_authenticated:
        # return Basket.objects.filter(user=user)
        return sum(list(Basket.objects.filter(user=user).values_list('quantity', flat=True)))
    return 0


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
    links_menu = ProductCategory.objects.all()
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
            'links_menu': links_menu,
            'category': category_item,
            'products': products_list,
            'basket': get_basket(request.user),
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = random.sample(list(Product.objects.all()), 1)[0]
    same_products = Product.objects.all().filter(
        category=hot_product.category).exclude(name=hot_product.name)
    context = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/products.html', context=context)
