# Generated by Django 5.1.4 on 2025-01-10 13:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0003_rename_reviews_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="image",
            field=models.ImageField(
                blank=True, default="default.jpg", null=True, upload_to=""
            ),
        ),
    ]
