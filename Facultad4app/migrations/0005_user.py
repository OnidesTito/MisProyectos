# Generated by Django 4.2.1 on 2023-06-04 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Facultad4app', '0004_prestamo'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=80, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=80, verbose_name='Apellidos')),
                ('username', models.CharField(max_length=80, unique=True, verbose_name='Usuario')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('role', models.CharField(default='Administrador', max_length=80, verbose_name='Rol')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
    ]
