from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm, PostForm
from django.utils import timezone
# from django.http import HttpResponseRedirect
from django.shortcuts import redirect
# Create your views here.


def post_list(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_details(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pk
            comment.published_date = timezone.now()
            comment.save()
            form = CommentForm()
            return render(request, 'blog/post_details.html', {'post': posts, 'form': form})
    else:
        form = CommentForm()
    return render(request, 'blog/post_details.html', {'post': posts, 'form': form})


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
