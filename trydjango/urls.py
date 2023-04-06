"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from meals.views import meal_queue_toggle_view
from search.views import search_view
from accounts.views import registration_view, logout_view, login_view
from .views import home_view, about

urlpatterns = [
#     path('', home_view, name="home"), # index / home / root
     path('about/', about, name='about'),
#     path('pantry/recipes/', include('recipes.urls')),
#     path('articles/', include('articles.urls')),
#     path('accounts/', include('accounts.urls')),
#     path('meal-toggle/<int:recipe_id>/', meal_queue_toggle_view, name='meal-toggle'),
    path('register/', registration_view, name='register'),
    path('logout', logout_view, name='logout'),
    path('login/', login_view, name='login'),
#     path('search/', search_view, name='search'),
#     #path('admin/', admin.site.urls),
 ]
