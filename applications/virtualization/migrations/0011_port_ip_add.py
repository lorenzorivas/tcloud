# Generated by Django 3.2.9 on 2021-12-06 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualization', '0010_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='port',
            name='ip_add',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
