from django.urls import path

from .views import (
    article_search_view,
    article_create_view,
    article_detail_view
)

app_name = 'articles'

#List of Article URLs with the format '(website-url)/(index)'
urlpatterns = [
    path('', article_search_view, name='search'),
    path('create/', article_create_view, name='create'),
    path('<slug:slug>/', article_detail_view, name='detail'),
]
