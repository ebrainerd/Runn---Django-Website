from django.db import models
from django.db import connections
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following

# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=False, default="")
    location = models.TextField(max_length=100, blank=False, default="")
    followers = models.ManyToManyField(User, symmetrical=False, related_name='is_following', blank=True) # user.is_following.all()

    objects = ProfileManager()

    def __str__(self):
    	return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # When a profile is created, have them follow the admin by default. # TODO: follow ALL admin users by default
        default_user_profile = Profile.objects.get(user__username__iexact='admin')
        default_user_profile.followers.add(instance)
        # TODO: Also have them follow themselves so they can see their own posts on home feed. 

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Post(models.Model):
	run_id = models.AutoField(primary_key=True)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	title = models.TextField(max_length=100, blank=False, default="")
	distance = models.FloatField(default=0.0, blank=False)
	time = models.IntegerField(default=0, blank=False)
	date_posted = models.DateTimeField(default=timezone.now)
	location = models.TextField(max_length=100, blank=False, default="")
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

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	comment_id = models.AutoField(primary_key=True)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['date_posted']

	def __str__(self):
		return 'Comment {} by {}'.format(self.content, self.author.first_name)
