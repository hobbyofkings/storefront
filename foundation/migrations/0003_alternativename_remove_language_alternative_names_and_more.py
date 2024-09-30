# Generated by Django 5.1.1 on 2024-09-30 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foundation', '0002_country_alter_language_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativeName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='language',
            name='alternative_names',
        ),
        migrations.AddField(
            model_name='language',
            name='alternative_names',
            field=models.ManyToManyField(blank=True, to='foundation.alternativename'),
        ),
    ]
