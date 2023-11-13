from django.db import models


# Create your models here.
class ChatModel(models.Model):
    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    time_stamp = models.DateTimeField(auto_now_add=True)
    time_stamps = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.message