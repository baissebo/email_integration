from django.contrib.auth.hashers import make_password, check_password
from django.db import models

from nullable import NULLABLE


class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class EmailMessage(models.Model):
    account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, verbose_name="Тема сообщения")
    date_sent = models.DateTimeField(verbose_name="Дата отправки")
    date_received = models.DateTimeField(auto_now_add=True, verbose_name="Дата получения")
    body = models.TextField(verbose_name="Тело сообщения")
    attachments = models.JSONField(default=list, verbose_name="Вложения", **NULLABLE)

    def __str__(self):
        return f"{self.subject}: {self.body[:20]}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-date_received"]
