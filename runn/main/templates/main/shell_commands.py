# This file can largely be ignored. It just helps clarify the follower model.
# https://www.codingforentrepreneurs.com/projects/try-django-111/follow-users
from django.contrib.auth.models import User

admin_user = User.objects.get(pk=1) 

# admin_user's followers
admin_user.profile.followers.all()

# who admin_user follows (reverse relationship) 
admin_user.is_following.all() # == admin_user.following.all()