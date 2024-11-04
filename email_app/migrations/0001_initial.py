# Generated by Django 5.1.2 on 2024-11-04 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmailAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="EmailMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject",
                    models.CharField(max_length=255, verbose_name="Тема сообщения"),
                ),
                ("date_sent", models.DateTimeField(verbose_name="Дата отправки")),
                (
                    "date_received",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата получения"
                    ),
                ),
                ("body", models.TextField(verbose_name="Тело сообщения")),
                (
                    "attachments",
                    models.JSONField(
                        blank=True, default=list, null=True, verbose_name="Вложения"
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="email_app.emailaccount",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ["-date_received"],
            },
        ),
    ]