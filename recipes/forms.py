from django import forms


from .models import Recipe, RecipeIngredient, RecipeIngredientImage, RecipeImage, RecipeReview

#Form to handle the upload of the Recipe Ingredient Image

class RecipeIngredientImageForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredientImage
        fields = ['image']
        labels = {
            "image": "Extract via Image Upload"
        }

#Form to handle the upload of the Recipe Image

class RecipeImageForm(forms.ModelForm):
    class Meta:
        model = RecipeImage
        fields = ['image']
        labels = {
            "image": "Upload image of your recipe here:"
        }

#Form to handle the upload of the Recipe

class RecipeForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    name = forms.CharField()
    # descriptions = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # django-crispy-forms
        for field in self.fields:
            new_data = {
                "placeholder": f'Recipe {str(field)}',
                "class": 'form-control',
                # "hx-post": ".",
                # "hx-trigger": "keyup changed delay:500ms",
                # "hx-target": "#recipe-container",
                # "hx-swap": "outerHTML"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        # self.fields['name'].label = ''
        # self.fields['name'].widget.attrs.update({'class': 'form-control-2'})
        self.fields['description'].widget.attrs.update({'rows': '2'})
        self.fields['directions'].widget.attrs.update({'rows': '4'})

#Form to handle the upload of the Recipe Ingredient

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']

#Form to handle the upload of the Recipe Review

class RecipeReviewForm(forms.ModelForm):
    class Meta:
        model = RecipeReview
        fields = ['subject', 'review', 'rating']