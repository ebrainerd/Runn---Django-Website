from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Post
from .models import Run


def home(request):
	context = {
		'posts': Run.objects.all()
	}

	# context = {
	# 	'runs': Run.objects.all()
	# }

	return render(request, 'main/home.html', context)

# class PostListView(ListView):
# 	model = Post
# 	template_name = 'main/home.html'  # <app>/<model>_<viewtpye>.html
# 	context_object_name = 'posts'
# 	ordering = ['-date_posted']


def about(request):
	return render(request, 'main/about.html', {'title': 'About'})

