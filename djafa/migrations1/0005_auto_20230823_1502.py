# Generated by Django 3.2.16 on 2023-08-23 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djafa', '0004_lignecomdraft_statut'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bl',
            name='codeCom',
        ),
        migrations.RemoveField(
            model_name='bl',
            name='codebl',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='codecom',
        ),
        migrations.RemoveField(
            model_name='facture',
            name='codebl',
        ),
        migrations.RemoveField(
            model_name='facture',
            name='codefac',
        ),
        migrations.RemoveField(
            model_name='lignebl',
            name='codebl',
        ),
        migrations.RemoveField(
            model_name='lignecom',
            name='codeCom',
        ),
        migrations.RemoveField(
            model_name='lignecomdraft',
            name='codeCom',
        ),
        migrations.RemoveField(
            model_name='lignefac',
            name='codefac',
        ),
        migrations.RemoveField(
            model_name='lignereglement',
            name='codereg',
        ),
        migrations.RemoveField(
            model_name='reglement',
            name='codefac',
        ),
        migrations.RemoveField(
            model_name='reglement',
            name='codereg',
        ),
    ]