# Generated by Django 5.1.1 on 2024-10-01 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foundation', '0013_demonym'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demonym',
            options={'ordering': ['country', 'main_demonym'], 'verbose_name': 'Demonym', 'verbose_name_plural': 'Demonyms'},
        ),
        migrations.RenameField(
            model_name='demonym',
            old_name='alternative_names',
            new_name='alternative_demonyms',
        ),
        migrations.RemoveField(
            model_name='demonym',
            name='language',
        ),
        migrations.RemoveField(
            model_name='demonym',
            name='normalized_name',
        ),
        migrations.AddField(
            model_name='demonym',
            name='main_demonym',
            field=models.CharField(blank=True, help_text='Demonym in English', max_length=255, null=True, unique=True),
        ),
    ]
