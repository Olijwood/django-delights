from django.urls import path

from .views import (
    recipe_list_view,
    recipe_user_list_view,
    recipe_detail_view,
    recipe_delete_view,
    recipe_create_view,
    recipe_update_view,
    recipe_detail_hx_view,
    recipe_ingredient_update_hx_view,
    recipe_ingredient_delete_view,
    recipe_ingredient_image_upload_view,
    recipe_image_upload_view,
    recipe_comments_view,
    recipe_submit_review_view,
)

app_name='recipes'

urlpatterns = [
    path("", recipe_list_view, name='list'),
    path("my-recipes/", recipe_user_list_view, name='my-list'),
    path("create/", recipe_create_view, name='create'),
    
    path("hx/<int:parent_id>/ingredient/<int:id>/", recipe_ingredient_update_hx_view, name='hx-ingredient-detail'),
    path("hx/<int:parent_id>/ingredient/", recipe_ingredient_update_hx_view, name='hx-ingredient-create'),
    path("hx/<int:id>/", recipe_detail_hx_view, name='hx-detail'),
    
    path("<int:parent_id>/ingredients/image-upload/", recipe_ingredient_image_upload_view, name='recipe-ingredient-image-upload'),
    path("<int:parent_id>/image-upload/", recipe_image_upload_view, name='recipe-image-upload'),
    path("<int:parent_id>/ingredient/<int:id>/delete/", recipe_ingredient_delete_view, name='ingredient-delete'),
    path('<int:id>/comment/', recipe_comments_view, name='comment'),
    path("<int:id>/delete/", recipe_delete_view, name='delete'),
    path("<int:id>/edit/", recipe_update_view, name='update'),
    path("<int:id>/submit-review/", recipe_submit_review_view ,name='submit-review'),
    path("<int:id>/", recipe_detail_view, name='detail'),
    
]