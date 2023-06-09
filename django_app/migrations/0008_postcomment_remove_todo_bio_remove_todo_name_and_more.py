# Generated by Django 4.1.3 on 2022-11-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0007_alter_todo_bio_alter_todo_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='todo',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='todo',
            name='name',
        ),
        migrations.AddField(
            model_name='todo',
            name='description',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='todo',
            name='title',
            field=models.CharField(blank=True, db_index=True, default='', max_length=150, null=True, unique=True, verbose_name='Заголовок'),
        ),
    ]
