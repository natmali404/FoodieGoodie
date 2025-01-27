from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from ..models import Uzytkownik, Forum, Post
from django.db.models import Count, Min
from ..forms.post_form import PostForm, ThreadForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View


class ForumAllView(ListView):
    model = Forum
    template_name = 'forum/forum_all.html'
    context_object_name = 'forums'

    def get_queryset(self):
        return Forum.objects.annotate(
            post_count=Count('posty'),
            data_zalozenia=Min('posty__dataDodaniaPostu')
        )
    

class ForumDetailView(DetailView):
    model = Forum
    template_name = 'forum/forum_detail.html'
    context_object_name = 'forum'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posty.order_by('dataDodaniaPostu')
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs): #new post creation
        self.object = self.get_object()  # needed for some reason
        forum = self.object
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = Post(
                trescPost=form.cleaned_data['trescPost'],
                obrazek=form.cleaned_data['obrazek'],
                forum=forum,
                glosy=0,
                autor=Uzytkownik.objects.get(idUzytkownik=1) # for debug purposes
            )
            post.save()
            return redirect('forum_detail', pk=forum.idForum)
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
    

class VotePostView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        vote_type = request.POST.get('vote_type')

        try:
            post = Post.objects.get(idPost=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

        if vote_type == 'upvote':
            post.glosy += 1
        elif vote_type == 'downvote':
            post.glosy -= 1
        else:
            return JsonResponse({'error': 'Invalid vote type'}, status=400)

        post.save()

        return JsonResponse({'new_vote_count': post.glosy})


class CreateThreadView(FormView):
    template_name = "forum/new_forum.html"
    success_url = reverse_lazy('forum_all')

    def get(self, request, *args, **kwargs):
        thread_form = ThreadForm()
        post_form = PostForm()
        return self.render_to_response({'thread_form': thread_form, 'post_form': post_form})

    def post(self, request, *args, **kwargs):
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST, request.FILES)

        if thread_form.is_valid() and post_form.is_valid():
            uzytkownik_1 = Uzytkownik.objects.get(idUzytkownik=1)

            forum = Forum.objects.create(
                tytulForum=thread_form.cleaned_data['tytulForum'],
                uzytkownik=uzytkownik_1
            )

            post = post_form.save(commit=False)
            post.forum = forum
            post.autor = uzytkownik_1
            post.glosy = 0
            print(post.__dict__)
            post.save()

            return self.form_valid(thread_form)
        
        return self.render_to_response({'thread_form': thread_form, 'post_form': post_form})


class EditPostView(UpdateView):
    model = Post
    fields = ['trescPost', 'obrazek']
    template_name = 'forum/edit_post.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('forum_detail', kwargs={'pk': self.object.forum.pk})
    
    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post
    
    
class DeletePostView(DeleteView):
    model = Post
    template_name = 'forum/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('forum_all')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()
        affected_forum = post.forum

        posts_count = Post.objects.filter(forum=affected_forum).count()
        
        context['posts_count'] = posts_count
        
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        affected_forum = post.forum

        post.delete()
        posts = Post.objects.filter(forum=affected_forum)
        
        if posts.count() == 0:
            affected_forum.delete()

        return HttpResponseRedirect(self.success_url)