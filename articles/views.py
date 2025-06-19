from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import (
    UpdateView, 
    DeleteView,
    CreateView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import ( 
    LoginRequiredMixin,
    UserPassesTestMixin
)


from django.views import View

from .models import Article
from .forms import CommentForm

# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'

class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = 'article_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        article = self.object
        return reverse('article_detail', kwargs={'pk': article.pk})

class CommentGet(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    
class CommentPost(View):
    pass

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'body')
    template_name = 'article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)