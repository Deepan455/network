from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass


class Posts(models.Model):
	creator = models.ForeignKey("Profile",related_name="profile",on_delete=models.CASCADE)
	content = models.CharField(blank=False, max_length=1000)
	timestamp = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)

	def __main__(self):
		return {
			"id":self.id,
			"creator":self.creator,
			"content":self.content,
			"timestamp":self.timestamp,
			"likes":self.likes
		}

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ForeignKey("Posts",related_name="posts",on_delete=models.CASCADE,null=True,blank=True	)
    followers = models.ManyToManyField("self",related_name="followers",blank=True)
    following = models.ManyToManyField("self",related_name="following",blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()