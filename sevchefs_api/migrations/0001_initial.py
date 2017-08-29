# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-29 14:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('upload_datetime', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('difficulty_level', models.IntegerField(default=0)),
                ('time_required', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serving_size', models.TextField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sevchefs_api.Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sevchefs_api.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeInstruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_num', models.IntegerField(default=1)),
                ('instruction', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Recipe', to='sevchefs_api.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=500, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='UserRecipeFavourites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sevchefs_api.Recipe')),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sevchefs_api.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='favourited_recipes',
            field=models.ManyToManyField(through='sevchefs_api.UserRecipeFavourites', to='sevchefs_api.Recipe'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='favourited_by',
            field=models.ManyToManyField(through='sevchefs_api.UserRecipeFavourites', to='sevchefs_api.UserProfile'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='sevchefs_api.RecipeIngredient', to='sevchefs_api.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='upload_by_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Recipes', to=settings.AUTH_USER_MODEL),
        ),
    ]
