# Generated by Django 4.2.7 on 2023-11-20 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tk', '0002_osoba_wlasciciel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='osoba',
            options={'permissions': [('can_view_other_persons', 'Can view other persons')]},
        ),
    ]
