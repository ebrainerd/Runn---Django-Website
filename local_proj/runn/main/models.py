from django.db import models
from django.db import connections
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


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
