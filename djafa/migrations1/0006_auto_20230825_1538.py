# Generated by Django 3.2.16 on 2023-08-25 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djafa', '0005_auto_20230823_1502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bl',
            old_name='idlignebl',
            new_name='idbl',
        ),
        migrations.AddField(
            model_name='lignebl',
            name='idlignebl',
            field=models.AutoField(default='', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bl',
            name='idcom',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='djafa.commande'),
        ),
        migrations.AlterField(
            model_name='lignebl',
            name='idlcom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djafa.lignecom'),
        ),
    ]