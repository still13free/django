from django.shortcuts import render


def main(request):
    context = {
        'title': 'Главная',
    }
    return render(request, 'mainapp/index.html', context=context)


links_menu = [
    {
        'url': 'products',
        'title': 'все',
    },
    {
        'url': 'products_home',
        'title': 'дом',
    },
    {
        'url': 'products_office',
        'title': 'офис',
    },
    {
        'url': 'products_modern',
        'title': 'модерн',
    },
    {
        'url': 'products_classic',
        'title': 'классика',
    },
]


def products(request):
    context = {
        'title': 'Продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', context=context)


def products_home(request):
    context = {
        'title': 'Продукты для дома',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', context=context)


def products_office(request):
    context = {
        'title': 'Продукты для офиса',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', context=context)


def products_modern(request):
    context = {
        'title': 'Продукты "модерн"',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', context=context)


def products_classic(request):
    context = {
        'title': 'Продукты "классика"',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', context=context)


def contacts(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contacts.html', context=context)
