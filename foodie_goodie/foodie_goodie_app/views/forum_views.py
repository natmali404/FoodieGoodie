from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from ..models import Uzytkownik, Forum, Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View


class ForumAllView(ListView):
    model = Forum
    template_name = 'forum/forum_all.html'
    context_object_name = 'forums'

    def get_queryset(self):
        return Forum.objects.all()
    