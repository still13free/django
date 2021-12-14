import random

from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render

from mainapp.models import Product, ProductCategory


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    return Product.objects.all().filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[:3]


def get_product_categories():
    return ProductCategory.objects.all()


def main(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4],
    }
    return render(request, 'mainapp/index.html', context=context)


def contacts(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contacts.html', context=context)


def products(request, pk=None, page=1):
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

        # page = request.GET.get('p', 1)
        paginator = Paginator(products_list, 3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        context = {
            'title': 'Продукты',
            'links_menu': get_product_categories(),
            'category': category_item,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'title': 'Продукты',
        'links_menu': get_product_categories(),
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': get_product_categories(),
    }
    return render(request, 'mainapp/product.html', context)
