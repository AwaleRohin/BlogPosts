from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import CommentForm, PostForm
from django.utils import timezone
from django.contrib import messages
# from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.


def category_list(request):
    cat = Category.objects.all()
    return render(request, 'blog/category_list.html', {'cat': cat})


def post_list(request, pk):
    posts = Category.objects.get(pk=pk).post_set.order_by("-id").all()
    return render(request, "blog/post_list.html", {'posts': posts})


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


# @login_required()
def post_create(request):
    # if request.method == "POST":
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.author = request.user
    #         post.published_date = timezone.now()
    #         post.save()
    #         messages.success(request, 'Sucessfully added')
    #         return redirect('post_details', pk=post.pk)
    # else:
    #     form = PostForm()
    # return render(request, 'blog/post_create.html', {'form': form})
    if request.method == "POST":
        if 'create' in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                cat = Category.objects.get(pk=request.POST['category'])
                post.category.add(cat)
                messages.success(request, 'Sucessfully added')
                return redirect('post_details', pk=post.pk)
        else:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                cat = Category.objects.get(pk=request.POST['category'])
                post.category.add(cat)
                messages.success(request, 'Sucessfully added')
                return redirect('post_drafts')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})


# @login_required()
def post_drafts(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_drafts.html', {'posts': posts})


# @login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'Sucessfully edited')
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pk
            comment.published_date = timezone.now()
            comment.save()
            form = CommentForm()
            return render(request, 'blog/post_details.html', {'post': post, 'form': form})
    else:
        form = CommentForm()
    return render(request, 'blog/post_details.html', {'post': post, 'form': form})


def publish(self):
    self.published_date = timezone.now()
    self.save()


# @login_required()
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.warning(request, 'Sucessfully deleted')
    return redirect('category_list')
