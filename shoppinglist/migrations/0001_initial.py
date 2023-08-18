# Generated by Django 4.2.4 on 2023-08-18 08:51

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
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, choices=[('pcs', 'Pieces'), ('pkgs', 'Packages'), ('kg', 'Kilogram'), ('g', 'Gram'), ('l', 'Liter'), ('ml', 'Milliliter')], max_length=20, null=True)),
                ('category', models.CharField(choices=[('fruits and vegetables', 'Fruits Vegetables'), ('meat', 'Meat'), ('diary', 'Diary'), ('dry goods', 'Dry Goods'), ('alcohols', 'Alcohols'), ('medicine', 'Medicine'), ('pet goods', 'Pet Goods'), ('baby goods', 'Baby Goods'), ('domestic detergents', 'Domestic Detergents'), ('ready-cook meals', 'Ready Cook Meals'), ('hygiene', 'Hygiene'), ('coffee & tea', 'Coffee Tea'), ('frozen foods', 'Frozen Foods'), ('garden and tinkering', 'Garden Tinker'), ('bread', 'Bread'), ('preserves', 'Preserves'), ('spices, sauces, additives', 'Spices'), ('fishes and seafood', 'Fish'), ('sweets and snacks', 'Sweets'), ('fats', 'Fats'), ('water and drinks', 'Drinks'), ('dried fruit and nuts', 'Nuts'), ('fresh herbs', 'Herbs'), ('canned food', 'Cans'), ('other', 'Other')], max_length=25)),
                ('note', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
                ('shoppinglist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppinglist.shoppinglist')),
            ],
            options={
                'ordering': ['completed'],
            },
        ),
    ]