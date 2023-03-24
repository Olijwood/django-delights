"""
To render html web pages
"""
import random
from django.http import HttpResponse
from django.template.loader import render_to_string
from articles.models import Article
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home_view(request):
    article_obj = Article.objects.get(id=1)
    article_queryset = Article.objects.all()
    context = {
        "title": article_obj.title,
        "content": article_obj.content,
        "object_list": article_queryset
    }
    return render(request, "home-view.html", context=context)