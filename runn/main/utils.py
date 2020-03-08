from django.utils import timezone
from datetime import timedelta
import pytz
from django.contrib.auth.models import User
from .models import Post

def statistics_last_7_days(User):
	qs = Post.objects.filter(author=User.profile,
							 date_posted__gte=timezone.now() - timedelta(days=7))
	miles = 0
	time = 0
	longest_run = 0
	fastest_pace = 0

	for post in qs:
		miles += post.distance
		time += post.time
		pace = round(post.time / post.distance, 2) if post.distance != 0 else 0

		if pace > fastest_pace:
			fastest_pace = pace
        
		if post.distance > longest_run:
			longest_run = post.distance

	avg_pace = round(time / miles, 2) if miles != 0 else 0

	return miles, time, avg_pace, longest_run, fastest_pace