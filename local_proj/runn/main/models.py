from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

class Run(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	distance = models.FloatField()
	time = models.IntegerField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	@property
	def pace(self):
		return round(self.time / self.distance, 2)

	def __str__(self):
		return self.title
