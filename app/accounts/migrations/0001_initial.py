# Generated by Django 3.1.5 on 2021-03-10 08:02

import accounts.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('email', models.EmailField(blank=True, editable=False, max_length=254, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(db_index=True, max_length=15, unique=True, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator(regex='[a-zA-Z0-9_]')], verbose_name='ユーザーネーム')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'カスタムユーザー',
                'verbose_name_plural': 'カスタムユーザー',
                'db_table': 't_custom_user',
            },
            managers=[
                ('objects', accounts.models.CustomUserManager()),
            ],
        ),
    ]
