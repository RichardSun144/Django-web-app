# Generated by Django 3.1.5 on 2021-02-03 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20210201_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='isDriver',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='DriverInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicleType', models.CharField(max_length=32)),
                ('licenseNumber', models.CharField(max_length=32)),
                ('containNumber', models.IntegerField()),
                ('specialText', models.TextField(blank=True, default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.userinfo')),
            ],
        ),
    ]
