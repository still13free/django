from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
# from mainapp.views import product


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    next_param = request.GET.get('next', '')
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)

            if 'next' in request.POST.keys():
                next_str = request.POST['next']

                if 'add' in next_str or 'remove' in next_str:
                    next_str = next_str.split('/')
                    pk = next_str[3]
                    return HttpResponseRedirect(reverse('products:products'))

                return HttpResponseRedirect(request.POST['next'])

            return HttpResponseRedirect(reverse('main'))
    context = {
        'login_form': login_form,
        'next': next_param,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('main'))

    else:
        register_form = ShopUserRegisterForm()
    context = {
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(
            request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
    context = {
        'edit_form': edit_form
    }
    return render(request, 'authapp/edit.html', context)
