from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import Http404
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
from .models import Post, Profile
from django.db.models import Q
from main.utils import user_statistics


class ProfileDetailView(DetailView):
    def get(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        if pk == request.user.pk:
            user_to_view = request.user
        elif pk is None:
            raise Http404("Could not get user.")
        else:
            user_to_view = get_object_or_404(User, id=pk, is_active=True)

        posts = Post.objects.filter(author=user_to_view.profile).order_by('-date_posted')
        is_following = False
        if self.request.user.is_authenticated and user_to_view.profile in self.request.user.is_following.all():
            is_following = True

        miles_last_7_days, time_last_7_days, avg_pace_last_7_days, longest_run_last_7_days, fastest_pace_last_7_days = \
            user_statistics(self.request.user, 99)

        context = {}
        context['posts'] = posts
        context['user'] = user_to_view
        context['is_following'] = is_following
        context['miles_last_7_days'] = miles_last_7_days
        context['time_last_7_days'] = time_last_7_days
        context['avg_pace_last_7_days'] = avg_pace_last_7_days
        context['longest_run_last_7_days'] = longest_run_last_7_days
        context['fastest_pace_last_7_days'] = fastest_pace_last_7_days

        # 'ou_' = other user's statistics (evaluated when viewing other user's profiles)
        if user_to_view.id != request.user.id:
            miles_last_7_days, time_last_7_days, avg_pace_last_7_days, longest_run_last_7_days, fastest_pace_last_7_days = \
                user_statistics(user_to_view, 9999)
            context['ou_miles_last_7_days'] = miles_last_7_days
            context['ou_time_last_7_days'] = time_last_7_days
            context['ou_avg_pace_last_7_days'] = avg_pace_last_7_days
            context['ou_longest_run_last_7_days'] = longest_run_last_7_days
            context['ou_fastest_pace_last_7_days'] = fastest_pace_last_7_days

        return render(request, 'main/profile.html', context)


class PostListViewHome(ListView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            qs = Post.objects.all().order_by('-date_posted')
            message = "You are not logged in. Displaying all posts by default. "\
                        + "Please sign in or register to search, view user profiles, and comment."
            messages.info(self.request, message)
            return render(request, 'main/home.html', {'posts': qs})

        Profile.objects.update_mileages(user)
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = Post.objects.filter(author__user__id__in=is_following_user_ids).order_by('-date_posted')
        if len(qs) == 0:
            messages.info(self.request, "There are no posts available to show. Follow other users or wait "
                          + "until one of the users you follow makes a post.")
        return render(request, 'main/home.html', {'posts': qs, 'user': user})


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
            Q(location__icontains = query)
        )
        context_dict = {'object_list': object_list, 'query': query}
    return render(request, 'main/search_users_location.html', context_dict)
