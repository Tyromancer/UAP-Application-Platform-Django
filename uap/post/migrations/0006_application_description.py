# Generated by Django 3.0.3 on 2020-04-06 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20200304_0640'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
    ]
