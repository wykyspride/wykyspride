# Generated by Django 3.2.16 on 2023-08-18 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djafa', '0002_auto_20230818_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bl',
            name='idcli',
        ),
        migrations.RemoveField(
            model_name='reglement',
            name='idcli',
        ),
        migrations.AddField(
            model_name='bl',
            name='client',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reglement',
            name='client',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='commande',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='facture',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='lignecomdraft',
            fields=[
                ('idlignedraf', models.AutoField(primary_key=True, serialize=False)),
                ('codeCom', models.CharField(default='', max_length=100)),
                ('qte', models.IntegerField(default=0)),
                ('prixu', models.DecimalField(decimal_places=2, default=0, max_digits=100000)),
                ('prixtotal', models.DecimalField(decimal_places=2, default=0, max_digits=100000)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('idprod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djafa.produit')),
            ],
            options={
                'verbose_name': 'Ligne Commande',
                'verbose_name_plural': 'Lignes Commande',
            },
        ),
    ]
