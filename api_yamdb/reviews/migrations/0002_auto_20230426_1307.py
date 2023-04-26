# Generated by Django 3.2 on 2023-04-26 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['name'], 'verbose_name': 'genre', 'verbose_name_plural': 'genres'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('-year',)},
        ),
        migrations.RemoveConstraint(
            model_name='title',
            name='unique_name_categories',
        ),
        migrations.RenameField(
            model_name='title',
            old_name='categories',
            new_name='category',
        ),
        migrations.AddConstraint(
            model_name='title',
            constraint=models.UniqueConstraint(fields=('name', 'category'), name='unique_name_category'),
        ),
    ]
