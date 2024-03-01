import random
from django.http import HttpResponse
from django.template.loader import render_to_string
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

#Home Page View
@login_required
def home_view(request):
    qs = Recipe.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "home-view.html", context)

#About Page View
def about(request):
    return render(request, "about.html")