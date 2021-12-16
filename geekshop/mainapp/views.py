import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from mainapp.models import Product, ProductCategory


def get_hot_product():
    return random.sample(list(get_all_products()), 1)[0]


def get_same_products(hot_product):
    return get_all_products().filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[:3]


def get_product_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category_item = cache.get(key)
        if category_item is None:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category_item)
        return category_item
    return get_object_or_404(ProductCategory, pk=pk)


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    return get_object_or_404(Product, pk=pk)


def get_all_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(
                is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


@cache_page(3600)
def main(request):
    context = {
        'title': 'Главная',
        'products': get_all_products()[:4],
    }
    return render(request, 'mainapp/index.html', context=context)


@cache_page(3600)
def contacts(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contacts.html', context=context)


def products(request, pk=None, page=1):
    links_menu = get_product_categories()
    if pk is not None:
        if pk == 0:
            products_list = get_all_products()
            category_item = {
                'name': 'все',
                'pk': 0,
            }
        else:
            category_item = get_category(pk)
            products_list = get_all_products().filter(category__pk=pk)

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
            'links_menu': links_menu,
            'category': category_item,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    context = {
        'product': get_product(pk),
        'links_menu': get_product_categories(),
    }
    return render(request, 'mainapp/product.html', context)
