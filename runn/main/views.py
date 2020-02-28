from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
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
from .forms import UserRegisterForm, CommentForm
from .models import Post, Profile, Comment
from django.db.models import Q

def home(request):
	context = {
		'posts': Post.objects.all()
	}

	return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html', {'title': 'About'})


def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	print("in func")
	print(post)


	if request.method == "POST":
		print("In post")
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post-detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'main/add_comment_to_post.html', {'form': form, 'post':post})


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


@login_required
def profile(request):
	return render(request, 'main/profile.html')

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
	success_url = '/'

	def form_valid(self, form):
		form.instance.author = self.request.user.profile
		return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content', 'distance', 'time']

	def form_valid(self, form):
		form.instance.author = self.request.user.profile
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
	def get_queryset(self):
		query = self.request.GET.get('q')
		object_list = Profile.objects.filter(
			Q(first_name__icontains=query)
			#Q(author__icontains = query)
		)
		return object_list