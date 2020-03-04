# Generated by Django 2.2.10 on 2020-03-04 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_uapuser_is_student'),
        ('post', '0002_auto_20200303_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UapUser')),
                ('urp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.URP')),
            ],
        ),
    ]
