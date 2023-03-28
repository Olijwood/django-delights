from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # model form for querysets
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from PIL import Image

from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientImageForm, RecipeImageForm
from .models import Recipe, RecipeIngredient, RecipeImage, Comment
from .services import extract_text_via_ocr_service
from .utils import (
    convert_to_qty_units,
    parse_paragraph_to_recipe_line
)
# CRUD -> Create Retrieve Update & Delete

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "recipes/list.html", context)

@login_required
def recipe_user_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "object_list": qs
    }
    return render(request, "recipes/my-list.html", context)


@login_required
def recipe_detail_view(request, id=None):
    hx_url = reverse("recipes:hx-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "recipes/detail.html", context) 


@login_required
def recipe_delete_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse('recipes:list')
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "recipes/delete.html", context)


@login_required
def recipe_ingredient_delete_view(request, parent_id=None, id=None):
    try:
        obj = RecipeIngredient.objects.get(recipe__id=parent_id, id=id, recipe__user=request.user)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404
    if request.method == "POST":
        name = obj.name
        obj.delete()
        success_url = reverse('recipes:detail', kwargs={"id": parent_id})
        if request.htmx:
            return render(request, "recipes/partials/ingredient-inline-delete-response.html", {"name": name})
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "recipes/delete.html", context)



@login_required
def recipe_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Recipe.objects.get(id=id)
    except:
        obj = None
    if obj is  None:
        return HttpResponse("Not found.")
    comments = obj.comments.all()
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            comment = Comment(recipe__id=obj.id, author=request.user, text=comment_text)
            comment.save()
    context = {
        "object": obj,
        'comments': comments,
    }
    return render(request, "recipes/partials/detail.html", context) 

@login_required
def recipe_comments_view(request, id=None):
    if request.method == "POST":
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return HttpResponseNotFound("Recipe not found")
        comment_text = request.POST.get('comment_text')
        if comment_text:
            comment = Comment(recipe=recipe, author=request.user, text=comment_text)
            comment.save()
    return redirect('recipes:detail', id=id)


@login_required
def recipe_rating_view(request, id=None):
    if request.method == 'POST':
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return HttpResponseNotFound("Recipe not found")

        rating = request.POST.get('rating')
        if rating is not None:
            try:
                rating = float(rating)
                if rating < 0 or rating > 10:
                    raise ValueError("Rating must be between 0 and 10")
            except ValueError:
                messages.error(request, "Invalid rating")
            else:
                if recipe.rating is not None:
                    recipe.rating = (recipe.rating + rating) / 2
                else:
                    recipe.rating = rating
                recipe.save()
                messages.success(request, "Thank you for rating this recipe")
        else:
            messages.error(request, "Rating is required")
    return redirect('recipes:detail', id=id)


@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse("Created", headers=headers)
            # context = {
            #     "object": obj
            # }
            # return render(request, "recipes/partials/detail.html", context)
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context)  

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    new_ingredient_url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id": obj.id})
    recipe_image = RecipeImage.objects.filter(recipe__id=id).last()
    image = 'recipes/images/default-pic.jpg'
    if recipe_image is not None:
        image = recipe_image.image
        print(image)
    context = {
        "form": form,
        "object": obj,
        "new_ingredient_url": new_ingredient_url,
        "image": image

    }
    if form.is_valid():
        form.save()
        context['message'] = 'Recipe Updated'
    if request.htmx:
        return render(request, "recipes/partials/forms.html", context)
    return render(request, "recipes/create-update.html", context)  


@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")
    instance = None
    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None
    form = RecipeIngredientForm(request.POST or None, instance=instance)
    url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "recipes/partials/ingredient-inline.html", context) 
    return render(request, "recipes/partials/ingredient-form.html", context) 



def recipe_ingredient_image_upload_view(request, parent_id=None):
    template_name = "recipes/ingredient-upload-image.html"
    if request.htmx:
        template_name = "recipes/partials/ingredient-image-upload-form.html"
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        raise Http404
    form = RecipeIngredientImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe = parent_obj
        # obj.recipe_id = parent_id
        obj.save()
        # send image file -> microservice api
        # microservice api -> data about the file
        # cloud providers $$
        extracted = extract_text_via_ocr_service(obj.image)
        obj.extracted = extracted
        obj.save()
        og = extracted['original']
        results = parse_paragraph_to_recipe_line(og)
        dataset = convert_to_qty_units(results)
        new_objs = []
        for data in dataset:
            data['recipe_id']  = parent_id
            new_objs.append(RecipeIngredient(**data))
        RecipeIngredient.objects.bulk_create(new_objs)
        success_url = parent_obj.get_edit_url()
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)

    return render(request, template_name, {"form":form})

import os
from PIL import Image
import secrets

def recipe_image_upload_view(request, parent_id=None):
    template_name = "recipes/upload-image.html"
    if request.htmx:
        template_name = "recipes/partials/image-upload-form.html"
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        raise Http404
    form = RecipeImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe_id = parent_id
        # obj.recipe_id = parent_id
        obj.save()
        success_url = parent_obj.get_edit_url()
        print(obj.image)
        print(obj.image.url)
        print(obj.recipe_id)
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)

    return render(request, template_name, {"form":form})