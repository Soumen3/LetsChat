from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class ChatModel(models.Model):
    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    time_stamp = models.DateTimeField(auto_now_add=True)
    time_stamps = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.message
    
class UserProfileModel(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(blank=True, null=True, max_length=50)
    online_status=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileModel.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender,instance, **kwargs):
    instance.userprofilemodel.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)