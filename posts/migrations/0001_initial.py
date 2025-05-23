# Generated by Django 5.2.1 on 2025-05-16 13:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Название', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Описание')),
                ('image', models.ImageField(blank=True, help_text='Загрузите картинку', upload_to='images/', verbose_name='Картинка')),
                ('category', models.CharField(choices=[('books', 'Книги'), ('electronics', 'Электроника'), ('cloth', 'Одежда'), ('furniture', 'Мебель'), ('other', 'Другое')], help_text='Выберете категорию', max_length=50)),
                ('condition', models.CharField(choices=[('new', 'Новое'), ('like new', 'Как новое'), ('used', 'Б/У'), ('for parts', 'На запчасти')], help_text='Выберете состояние', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ExchangeProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(help_text='Комментарий')),
                ('status', models.CharField(choices=[('pending', 'На рассмотрении'), ('accepted', 'Принято'), ('rejected', 'Отклонено')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_proposals', to='posts.post')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_proposals', to='posts.post')),
            ],
        ),
    ]
