# Generated by Django 5.0.6 on 2024-05-23 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='users/'),
        ),
    ]
