from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from .models import Post, Profile, Comment
from django.db.models import Q


class PostListView(ListView):
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            qs = Post.objects.all().order_by('-date_posted')
            messages.info(self.request, "You are not logged in. Displaying all posts.")
            return render(request, 'main/home.html', {'posts': qs})

        user = request.user
        Profile.objects.update_mileages(user)
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = Post.objects.filter(author__user__id__in=is_following_user_ids).order_by('-date_posted')
        if len(qs) == 0:
            messages.info(self.request, "There are no posts available to show. Follow other users or wait "
                          + "until one of the users you follow makes a post.")
        return render(request, 'main/home.html', {'posts': qs, 'user': user})


class PostListViewProfile(ListView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = request.user
            Profile.objects.update_mileages(user)
            user_posts = Post.objects.filter(author=user.profile).order_by('-date_posted')
            if len(user_posts) == 0:
                messages.info(self.request, "Post something!")
            return render(request, 'main/profile.html', {'posts': user_posts, 'user': user})

        else:
            messages.info(self.request, "Login to use see your friends' updates")
            return render(request, 'main/profile.html', {'posts': {}})


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
        if self.request.user.profile == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.profile
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'main/add_comment_to_post.html', {'form': form, 'post': post})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user.refresh_from_db()  # load the profile instance created by the signal
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
    return render(request, 'main/register.html', {'form': form})


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)

        return redirect('user-profile', profile_.user.id)


@login_required
def update_profile(request, pk):
    if not request.user.id == pk:  # pk is the primary key of the user being edited
        messages.info(request, f'You cannot edit another user\'s account.')
        return redirect('user-profile', pk)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-profile', pk)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main/profile_update.html', context)


def search(request):
    return render(request, 'main/search.html', {'title': 'Search'})


def search_users_name(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        object_list = find_user_by_first_and_last_name(query)
    context_dict = {'object_list': object_list, 'query': query}
    return render(request, 'main/search_users_name.html', context_dict)


def find_user_by_first_and_last_name(query_name):
    qs = Profile.objects.all()
    for term in query_name.split():
        qs = qs.filter(Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term) | Q(
            user__username__icontains=term))
    return qs


def search_users_location(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        object_list = Profile.objects.filter(
            Q(location__icontains=query)
        )
        context_dict = {'object_list': object_list, 'query': query}
    return render(request, 'main/search_users_location.html', context_dict)
