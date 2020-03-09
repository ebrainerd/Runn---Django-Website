from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Post

def user_statistics(user_, days_to_subtract=None):
	if days_to_subtract is None:
		qs = Post.objects.filter(author=user_.profile)
	else:
		qs = Post.objects.filter(author=user_.profile,
							 	date_posted__gte=timezone.now() - timedelta(days=days_to_subtract))
	miles = 0
	time = 0
	longest_run = 0
	fastest_pace = 999999 # some large integer

	for post in qs:
		miles += post.distance
		time += post.time_minutes
		pace = round(post.time_minutes / post.distance, 2) if post.distance != 0 else 0

		if pace < fastest_pace:
			fastest_pace = pace
        
		if post.distance > longest_run:
			longest_run = post.distance

	avg_pace = round(time / miles, 2) if miles != 0 else 0

	return miles, time, avg_pace, longest_run, fastest_pace
