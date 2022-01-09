from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from basketapp.models import Basket
from mainapp.models import Product
from django.db.models import F


def get_baskets_list(user):
    return Basket.objects.filter(user=user).select_related()


@login_required
def basket(request):
    context = {
        'basket': get_baskets_list(request.user)
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def add(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(
        product=product_item, user=request.user).first()

    if not basket_item:
        basket_item = Basket(product=product_item, user=request.user)

    basket_item.quantity = F('quantity') + 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

    context = {
        'basket': get_baskets_list(request.user)
    }
    result = render_to_string(
        'basketapp/includes/inc_baskets_list.html', context)
    return JsonResponse({'result': result})
