# Generated by Django 4.2.5 on 2023-11-25 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion1', '0010_preguntasrespondidas_retroalimentacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preguntasrespondidas',
            name='retroalimentacion',
        ),
        migrations.AddField(
            model_name='preguntas',
            name='retroalimentacion',
            field=models.TextField(blank=True, verbose_name='Retroalimentación'),
        ),
    ]
