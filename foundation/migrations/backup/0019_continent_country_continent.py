# Generated by Django 5.1.1 on 2024-10-03 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foundation', '0018_administrativeunittype_alter_currencyperiod_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Continent',
                'verbose_name_plural': 'Continents',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='country',
            name='continent',
            field=models.CharField(blank=True, choices=[('AF', 'Africa'), ('AN', 'Antarctica'), ('AS', 'Asia'), ('EU', 'Europe'), ('NA', 'North America'), ('OC', 'Oceania'), ('SA', 'South America')], help_text='Continent of the country', max_length=2, null=True),
        ),
    ]