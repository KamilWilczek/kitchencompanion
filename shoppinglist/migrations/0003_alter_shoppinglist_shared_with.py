# Generated by Django 4.2.5 on 2023-09-25 18:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shoppinglist', '0002_shoppinglist_shared_with'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_shopping_lists', to=settings.AUTH_USER_MODEL),
        ),
    ]