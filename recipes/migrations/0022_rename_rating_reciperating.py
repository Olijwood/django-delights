# Generated by Django 3.2.18 on 2023-03-29 22:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0021_alter_rating_rating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rating',
            new_name='RecipeRating',
        ),
    ]