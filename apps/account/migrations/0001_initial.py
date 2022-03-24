# Generated by Django 4.0.3 on 2022-03-24 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
                ('bio', models.CharField(max_length=800)),
                ('profile_photo', models.ImageField(default='media/avatar/ava.png', null=True, upload_to='media/avatars/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]