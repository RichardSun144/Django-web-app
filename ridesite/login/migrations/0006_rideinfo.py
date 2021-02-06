# Generated by Django 3.1.5 on 2021-02-06 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20210203_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='RideInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('startPoint', models.CharField(max_length=32)),
                ('endPoint', models.CharField(max_length=32)),
                ('memberNumber', models.IntegerField()),
                ('specialText', models.TextField(blank=True, default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.userinfo')),
            ],
        ),
    ]