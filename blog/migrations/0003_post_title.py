# Generated by Django 5.1.4 on 2024-12-15 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_remove_post_likes_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="title",
            field=models.CharField(default="Заголовок", max_length=50),
        ),
    ]
