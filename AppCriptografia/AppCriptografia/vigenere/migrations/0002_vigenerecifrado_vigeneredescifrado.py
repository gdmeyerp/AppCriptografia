# Generated by Django 5.1.4 on 2024-12-06 05:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vigenere', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VigenereCifrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje_original', models.TextField()),
                ('clave', models.CharField(max_length=255)),
                ('mensaje_cifrado', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VigenereDescifrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje_cifrado', models.TextField()),
                ('clave', models.CharField(max_length=255)),
                ('mensaje_descifrado', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
