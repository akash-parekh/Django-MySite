from datetime import date

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post
from .forms import CommentForm

# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset =  super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


class PostDetailView(View):
    
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post.id in stored_posts
        else:
            is_saved_for_later = False

        context = {
            "post":post,
            "post_tags":post.caption.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id"),
            "is_saved_for_later": is_saved_for_later
        }
        return render(request, 'blog/post-detail.html', context)
    
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post.id in stored_posts
        else:
            is_saved_for_later = False

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-details-page", args=[slug]))
        
        context = {
            "post":post,
            "post_tags":post.caption.all(),
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id"),
            "is_saved_for_later": is_saved_for_later
        }
        return render(request, 'blog/post-detail.html', context)
    
class ReadLaterView(View):
    
    def get(self, request):
        stored_post = request.session.get("stored_posts")
        context = {}
        if stored_post is None or len(stored_post) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_post)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)
    
    def post(self, request):
        stored_post = request.session.get("stored_posts")
        
        if stored_post is None:
            stored_post = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)

        request.session["stored_posts"] = stored_post

        return HttpResponseRedirect("/")