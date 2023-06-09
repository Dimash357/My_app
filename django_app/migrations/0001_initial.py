# Generated by Django 4.1.3 on 2022-11-14 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, db_index=True, default='', max_length=150, unique=True, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Публикации',
                'ordering': ('id',),
            },
        ),
    ]
