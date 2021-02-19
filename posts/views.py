from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from . import models
from . import forms
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count

# Create your views here.
def post_list(request):
    # Input Parameter
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw',)

    #Sort
    search_option = request.GET.get('search_option', 'recent')  #default

    if search_option == 'recommend':
        post_list = models.Post.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif search_option == 'popular':
        post_list = models.Post.objects.annotate(num_comment=Count('comment')).order_by('-num_comment','-create_date')
    else:
        post_list = models.Post.objects.order_by('-create_date')

    # Look up
   
    if kw:
        post_list = post_list.filter(
            Q(title__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) 
        ).distinct()

    paginator=Paginator(post_list, 15)
    page_obj = paginator.get_page(page)

    context = {'post_list':page_obj, 'page':page, 'kw':kw}

    return render(request, 'posts/post_list.html', context)

class post_detail(generic.DetailView):
    model = models.Post
    context_object_name = 'post_detail'
    template_name = 'posts/post_detail.html'

@login_required(login_url='accounts:login')
def create_post(request):
    if request.method == 'POST':
        form = forms.Create_Post_Form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.create_date = timezone.now()
            post.author = request.user
            post.save()
            return redirect('posts:post_list')
    else:
        form = forms.Create_Post_Form()
    context = {'form':form}
    return render(request, 'posts/create_post.html', context)
    
@login_required(login_url='accounts:login')
def add_comment_to_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_date = timezone.now()
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('posts:detail', pk = pk), comment.id))
    else:
        form = forms.CommentForm()

    context = {'post':post, 'form':form}
    return render(request, 'posts/post_list.html', context)

@login_required(login_url='accounts:login')
def post_modify(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    
    if request.method == "POST":
        form = forms.Create_Post_Form(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.modify_date = timezone.now()
            post.save()
            return redirect('posts:detail', pk = pk)
    else:
        form = forms.Create_Post_Form(instance=post)
    context = {'form':form}
    return render(request, 'posts/create_post.html', context)


@login_required(login_url='accounts:login')
def post_delete(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    
    post.delete()
    return redirect('posts:post_list')

@login_required(login_url='accounts:login')
def comment_delete(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    
    comment.delete()
    return redirect('posts:detail', pk=comment.post.pk)

@login_required(login_url='accounts:login')
def vote_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if post.voter.filter(pk=request.user.id).exists():
        post.voter.remove(request.user)
    else:
        post.voter.add(request.user)
    return redirect('posts:detail', pk=post.pk)

@login_required(login_url='accounts:login')
def vote_comment(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    if comment.voter.filter(pk=request.user.id).exists():
        comment.voter.remove(request.user)
    else:
        comment.voter.add(request.user)
    return redirect('{}#comment_{}'.format(
                resolve_url('posts:detail', pk = comment.post.pk), comment.id))