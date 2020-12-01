from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    #followers = models.ManyToManyField("self",related_name="following",blank=True)
    following = models.ManyToManyField("self",symmetrical=False,related_name="followers",blank=True)
    pass

class Posts(models.Model):
	creator = models.ForeignKey("User",related_name="profile",on_delete=models.CASCADE)
	content = models.CharField(blank=False, max_length=1000)
	timestamp = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)
	likedby = models.ManyToManyField("User",related_name="likers",blank=True)

	def __main__(self):
		return {
			"id":self.id,
			"creator":self.creator,
			"content":self.content,
			"timestamp":self.timestamp,
			"likes":self.likes,
			"likedby":self.likedby
		}

class Image(models.Model):
	uploader = models.ForeignKey("User", related_name="pics", on_delete=models.CASCADE)
	post= models.ForeignKey("Posts", related_name="pics", on_delete=models.CASCADE)
	link = models.CharField(blank=False, max_length=1000)
	code = models.CharField(blank=False, max_length=200)

	def __main__(self):
		return{
		"id":self.id,
		"uploader":self.uploader,
		"post":self.post,
		"link":self.link,
		"code":self.code
		}