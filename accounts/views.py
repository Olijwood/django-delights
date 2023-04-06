from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import Http404, HttpResponse
from django.urls import reverse

from .forms import RegistrationForm, AccountAuthenticationForm, UpdateAccountForm, AccountImageForm
from .models import Account
from recipes.models import Recipe
# Create your views here.

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['form'] = form
    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'accounts/register.html', context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login/")
    return render(request, "accounts/logout.html", {})

def login_view(request):
    context = {}
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['form'] = form
    return render(request, 'accounts/login.html', context)

def account_view(request, id=None):
    try:
        user = Account.objects.get(id=id)
    except:
        user = None
    if user is None:
        raise Http404
    try:
        recipes_list = Recipe.objects.filter(user_id=id)
    except:
        user = None
    form = UpdateAccountForm(instance=user)
    image_form = AccountImageForm(request.POST or None, request.FILES or None)
    if request.POST:
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        success_url = reverse("accounts:account", kwargs={"id": id})
        return redirect(success_url)
    context = {
        'account': user,
        "form": form,
        "image_form": image_form,
        "object_list": recipes_list
    }
    return render(request, 'accounts/account.html', context)

def account_image_upload_view(request, id=None):
    template_name = "accounts/upload-image.html"
    if request.htmx:
        template_name = "accounts/partials/image-upload-form.html"
    try:
        user = Account.objects.get(id=id)
    except:
        user = None
    if user is None:
        raise Http404
    image_form = AccountImageForm(request.POST or None, request.FILES or None)
    if image_form.is_valid():
        print('is valid')
        obj = image_form.save(commit=False)
        obj.account_id = user.id
        obj.save()
        success_url = reverse('accounts:account', kwargs={'id': id})
        print(obj.image)
        print(obj.image.url)
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)
    return render(request, template_name, {"form": image_form})