# Generated by Django 5.0.3 on 2024-03-26 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wireguard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interface',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='interface',
            name='subnet',
        ),
        migrations.RemoveField(
            model_name='peer',
            name='ip_address',
        ),
    ]
