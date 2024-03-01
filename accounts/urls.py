from django.urls import path

from .views import account_view, account_image_upload_view

app_name = 'accounts'

#List of Account URLs with the format '(website-url)/(index)'

urlpatterns = [
    path('<int:id>/account/', account_view, name='account'),
    path('<int:id>/image-upload/>', account_image_upload_view, name="image-upload")
]