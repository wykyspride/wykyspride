# Generated by Django 3.2.16 on 2023-08-18 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djafa', '0003_auto_20230818_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignecomdraft',
            name='statut',
            field=models.CharField(default='draft', max_length=10),
        ),
    ]