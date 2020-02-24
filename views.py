from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Post, Profile
from django.db.models import Q

def home(request): 
	context = {
		'posts': Post.objects.all()
	}

	return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html', {'title': 'About'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('main-home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form' : form})

class PostListView(ListView):
	model = Post
	template_name = 'main/home.html'  # <app>/<model>_<viewtpye>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']


class PostDetailView(DetailView):
	model = Post

class PostCreateView(CreateView):
	model = Post
	fields = ['title', 'content', 'distance', 'time']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content', 'distance', 'time']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True

		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True

		return False


class SearchResultsView(ListView):
	model = Profile
	template_name = 'main/search.html'
	#queryset = Run.objects.filter(title__icontains = 'run')
	#def get_queryset(self):
	#	query = self.request.GET.get('q')
	#	object_list = Profile.objects.filter(
	#		Q(first_name__icontains=query)
	#		#Q(author__icontains = query)
	#	)
	#	return object_list

