from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post  # .models means current package's models
# Create your views here.

'''
def home(request):
    context = {
        # query for our database
        'posts': Post.objects.all()
    }
    # blog refers to sub dir in templates dir
    return render(request, 'blog/home.html', context)'''


class PostListView(ListView):
    model = Post  # what model we want to query for the list
    template_name = 'blog/home.html'  # changing default template to one we alr. made
    context_object_name = 'posts'  # posts is the name we give to the objects queried from model=Post
    # orders posts from newest to oldest based on date
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted'] <-- will be overriden by function below since we are overriding the query
    paginate_by = 5

    def get_queryset(self):
        # override the query set to return Post objects that have a specific usernamess
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post  # what model we want to query for the list


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post  # what model we want to query for the list
    fields = ['title', 'content']

    def form_valid(self, form):  # overriding form method
        # sets author to current user, then validates form
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):  # returns to homepage after creating a new post
        return reverse('blog-home', kwargs={})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post  # what model we want to query for the list
    fields = ['title', 'content']
    success_url = '/'  # returns to homepage after creating post

    def form_valid(self, form):  # overriding form method
        # sets author to current user, then validates form
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  # UserPassesTestMixin will run to see if cur. user passes certain conditions
        post = self.get_object()  # gets post we are trying to update (provided by UpdateView)
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post  # what model we want to query for the list
    success_url = '/'  # returns to homepage after deleting post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    '''def get_success_url(self):  # returns to homepage after deleting a new post
        return reverse('blog-home', kwargs={})'''


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
