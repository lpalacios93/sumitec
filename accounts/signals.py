from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        role = UserProfile.Role.ADMIN if instance.is_superuser else UserProfile.Role.SELLER
        must_change_password = not instance.is_superuser
        UserProfile.objects.create(
            user=instance,
            role=role,
            must_change_password=must_change_password,
        )
        return

    profile, _ = UserProfile.objects.get_or_create(user=instance)
    if instance.is_superuser and profile.role != UserProfile.Role.ADMIN:
        profile.role = UserProfile.Role.ADMIN
        profile.save(update_fields=["role", "updated_at"])
