from django.db import models
from django.db import connections
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=50, blank=False, default="")
    last_name = models.TextField(max_length=50, blank=False, default="")
    email = models.TextField(max_length=75, blank=False, default="")
    bio = models.TextField(max_length=500, blank=False, default="")
    location = models.TextField(max_length=100, blank=False, default="")
    user_type = models.IntegerField(default=0, blank=False) # 0 is regular user, 1 is coach 

class Post(models.Model):
	run_id = models.AutoField(primary_key=True)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	title = models.TextField(max_length=100, blank=False, default="title holder.")
	distance = models.FloatField(default=0.0, blank=False)
	time = models.IntegerField(default=0, blank=False)
	date_posted = models.DateTimeField(default=timezone.now)
	location = models.TextField(max_length=100, blank=False, default="")
	image = models.TextField(max_length=250, blank=True)
	content = models.TextField(max_length=1000, blank=True, default="")

	@property
	def pace(self):
		if self.distance == 0.0:
			return 0.0
		return round(self.time / self.distance, 2)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Comment(models.Model):
	comment_id = models.AutoField(primary_key=True)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	run_id = models.ForeignKey(Post, on_delete=models.CASCADE) 
	content = models.TextField(max_length=1000, blank=False, default="")
	date_posted = models.DateTimeField(default=timezone.now)

class Following(models.Model):
	UserID_Following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
	UserID_Followee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')

