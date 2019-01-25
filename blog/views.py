from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm
from django.utils import timezone
from django.http import HttpResponseRedirect
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
            return HttpResponseRedirect('/%d' % int(pk), {'post': posts, 'form': form})
    else:
        form = CommentForm()
    return render(request, 'blog/post_details.html', {'post': posts, 'form': form})
