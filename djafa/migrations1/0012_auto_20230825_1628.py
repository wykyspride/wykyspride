# Generated by Django 3.2.16 on 2023-08-25 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djafa', '0011_auto_20230825_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lignebl',
            name='bl',
        ),
        migrations.RemoveField(
            model_name='lignebl',
            name='idcom',
        ),
        migrations.RemoveField(
            model_name='lignebl',
            name='idlcom',
        ),
        migrations.RemoveField(
            model_name='lignebl',
            name='idprod',
        ),
        migrations.RemoveField(
            model_name='facture',
            name='bl',
        ),
        migrations.RemoveField(
            model_name='reglement',
            name='bl',
        ),
        migrations.DeleteModel(
            name='bl',
        ),
        migrations.DeleteModel(
            name='lignebl',
        ),
    ]
