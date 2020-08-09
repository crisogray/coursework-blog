from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, CVEntry
from .forms import PostForm, CVEntryForm


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def cv_page(request):
    bio = CVEntry.objects.filter(section=0)
    education = CVEntry.objects.filter(section=1).filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    workexp = CVEntry.objects.filter(section=2).filter(
        published_date__lte=timezone.now()).order_by('start_date')
    skills = CVEntry.objects.filter(section=3).filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    interests = CVEntry.objects.filter(section=4).filter(
        published_date__lte=timezone.now()).order_by('published_date')
    misc = CVEntry.objects.filter(section=5).filter(
        published_date__lte=timezone.now()).order_by('published_date')
    return render(
        request, 'blog/cv.html', {
            'bio': bio,
            'education': education,
            'workexp': workexp,
            'skills': skills,
            'interests': interests,
            'misc': misc
        })


def cv_new(request):
    if request.method == "POST":
        form = CVEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            entry.publish()
            return redirect('cv_new')
    else:
        form = CVEntryForm()
    return render(request, 'blog/cv_new.html', {'form': form})
