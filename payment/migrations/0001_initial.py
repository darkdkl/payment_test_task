# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-06-08 16:20
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import payment.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефон')),
                ('first_last_name', models.CharField(max_length=250, verbose_name='Имя и Фамилия')),
                ('total_payment', models.FloatField(default=0, verbose_name='Общее вознаграждение')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', payment.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма выплаты')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки ')),
                ('date_processing', models.DateTimeField(blank=True, null=True, verbose_name='Дата обработки заявки')),
                ('paid_out', models.BooleanField(default=False, verbose_name='Выплачено')),
                ('invoice', models.TextField(blank=True, null=True, verbose_name='Номер счёта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма платежа')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
    ]
