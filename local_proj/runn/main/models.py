from django.db import models
from django.db import connections
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	distance = models.FloatField(default=0.0)
	time = models.IntegerField(default=0)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	@property
	def pace(self):
		return round(self.time / self.distance, 2)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=50, blank=True)
    last_name = models.TextField(max_length=50, blank=True)
    email = models.TextField(max_length=75, blank=True)
    tagline = models.TextField(max_length=250, blank=True)
    location = models.TextField(max_length=100, blank=True)
    user_type = models.IntegerField(default=0) # 0 is regular user, 1 is coach 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    


