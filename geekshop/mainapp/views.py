from django.shortcuts import render

from mainapp.models import Product, ProductCategory


def main(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    context = {
        'title': 'Продукты',
        'links_menu': ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/products.html', context=context)


def contacts(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contacts.html', context=context)
