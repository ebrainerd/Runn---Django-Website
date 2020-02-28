from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
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
from django.contrib.auth.models import User
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
            user = form.save()
            username = form.cleaned_data.get('username')
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.location = form.cleaned_data.get('location')
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('main-home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form' : form})


def search(request):
	print (" serarch")
	query = request.GET.get('q')
	object_list = Profile.objects.filter(
		Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(user__username__icontains=query)
	)
	context_dict = {'object_list': object_list, 'query': query}
	return render(request, 'main/search.html', context_dict)

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

#class SearchResultsView(ListView):
	#model = Profile
	#template_name = 'main/search.html'
	def search(request):
		print (" serarch")
		query = request.GET.get('q')
		object_list = Profile.objects.filter(
			Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(user__username__icontains=query) | Q(user__location__icontains=query)
		)
		context_dict = {'object_list': object_list, 'query': query}
		return render(request, 'main/search.html', context_dict)

	#def get_queryset(self):
	#	print ("Get query")
	#	query = self.request.GET.get('q')
	#	object_list = Profile.objects.filter(
	#		Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(user__username__icontains=query)
	#	)
	#	return object_list
