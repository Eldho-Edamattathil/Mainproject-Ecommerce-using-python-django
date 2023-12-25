from userauths.models import User
from .models import UserDetails
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
  if created:
    UserDetails.objects.create(user=instance)