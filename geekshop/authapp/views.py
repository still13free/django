from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from authapp.forms import (ShopUserEditForm, ShopUserLoginForm,
                           ShopUserProfileEditForm, ShopUserRegisterForm)
from authapp.models import ShopUser


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
            new_user = register_form.save()
            send_verify_email(new_user)
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
        edit_profile_form = ShopUserProfileEditForm(
            request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        edit_profile_form = ShopUserProfileEditForm(
            instance=request.user.shopuserprofile)
    context = {
        'edit_form': edit_form,
        'edit_profile_form': edit_profile_form
    }
    return render(request, 'authapp/edit.html', context)


def verify(request, email, key):
    # user = get_object_or_404(ShopUser, email=email)
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activate_key == key and not user.is_activate_key_expired():
            user.activate_user()
            auth.login(request, user)
    return render(request, 'authapp/register_result.html')


def send_verify_email(user):
    verify_link = reverse('authapp:verify', args=(
        user.email, user.activate_key))
    full_link = f'{settings.BASE_URL}{verify_link}'

    message = f'Your activation url: {full_link}'
    return send_mail(
        'Account activation',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
