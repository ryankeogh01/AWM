from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models



# class Profile(models.Model):
#         user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
#         created = models.DateTimeField(auto_now_add=True, editable=False)
#         modified = models.DateTimeField(auto_now=True, editable=False)
#         last_location = models.PointField(editable=False, blank=True, null=True, default=None)
#
#         def __str__(self):
#             return f"{self.user}"
#
# Signal

class Profile(models.Model):
    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    last_location = models.PointField(verbose_name="last_location", editable=False, blank=True, null=True, default=None, help_text=(
            "Geographic coordinates (lon/lat) as Point. Can be serialised from WKT (well-known text) representation")
                                      )

    def __str__(self):
        return f"{self.user}"

@receiver(post_save, sender=get_user_model())
def manage_user_profile(sender, instance, created, **kwargs):
    try:
        my_profile = instance.profile
        my_profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
