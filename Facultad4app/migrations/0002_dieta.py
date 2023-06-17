# Generated by Django 4.2.1 on 2023-05-18 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Facultad4app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dieta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('lastname', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('fechaI', models.DateField(verbose_name='Fecha Inicio de la dieta')),
                ('fechaF', models.DateField(verbose_name='Fecha Fin de la dieta')),
                ('CI', models.CharField(verbose_name='CI')),
                ('desc', models.TextField(verbose_name='Descripcion')),
            ],
        ),
    ]
