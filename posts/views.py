from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView, UpdateView
from django.views.generic.edit import CreateView

from .models import STATUS_CHOICES, ExchangeProposal, Post


class PostListView(ListView):
    model = Post
    template_name = "posts/posts.html"
    context_object_name = "posts"
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self) -> QuerySet[Post]:
        queryset = Post.objects.all()
        query = self.request.GET.get("q")
        category = self.request.GET.get("category")
        condition = self.request.GET.get("condition")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return {
            **super().get_context_data(**kwargs),
            "categories": Post.CATEGORY_CHOICES.choices,
            "conditions": Post.CONDITION_CHOICES.choices,
        }


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/new_post.html"
    fields = ["title", "description", "image", "category", "condition"]
    success_url = reverse_lazy("posts:my_posts")
    login_url = "posts:login"

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class MyPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/my_posts.html"
    context_object_name = "posts"
    paginate_by = settings.PAGINATE_BY
    login_url = "posts:login"

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.filter(user=self.request.user)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "description", "image", "category", "condition"]
    template_name = "posts/new_post.html"
    success_url = reverse_lazy("posts:my_posts")
    login_url = "posts:login"

    def get_object(self, queryset=None) -> Post | None:
        post = super().get_object(queryset)
        if post.user != self.request.user:
            raise PermissionDenied(
                "Вы не можете редактировать чужое объявление."
            )
        return post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/delete_post.html"
    success_url = reverse_lazy("posts:my_posts")
    login_url = "posts:login"

    def get_object(self, queryset=None) -> Post | None:
        post = super().get_object(queryset)
        if post.user != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужое объявление.")
        return post


class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    fields = ["receiver", "comment"]
    template_name = "proposals/proposal_form.html"
    success_url = reverse_lazy("posts:posts_list")
    login_url = "posts:login"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        post_id = self.request.GET.get("post_id")
        if post_id:
            receiver = get_object_or_404(Post, id=post_id)
            initial["receiver"] = receiver
        return initial

    def form_valid(self, form) -> HttpResponse:
        sender_post_id = self.request.POST.get("sender_post_id")
        sender = get_object_or_404(
            Post, id=sender_post_id, user=self.request.user
        )
        form.instance.sender = sender
        form.instance.receiver = form.instance.receiver
        return super().form_valid(form)


class MyProposalsListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = "proposals/my_proposals_list.html"
    context_object_name = "proposals"
    paginate_by = settings.PAGINATE_BY
    login_url = "posts:login"

    def get_queryset(self) -> QuerySet[ExchangeProposal]:
        queryset = ExchangeProposal.objects.filter(
            Q(sender__user=self.request.user)
            | Q(receiver__user=self.request.user)
        ).select_related(
            "sender", "receiver", "sender__user", "receiver__user"
        )
        sender_id = self.request.GET.get("sender")
        receiver_id = self.request.GET.get("receiver")
        status = self.request.GET.get("status")

        if sender_id:
            queryset = queryset.filter(sender__user__id=sender_id)
        if receiver_id:
            queryset = queryset.filter(receiver__user__id=receiver_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        queryset = ExchangeProposal.objects.filter(
            Q(sender__user=self.request.user)
            | Q(receiver__user=self.request.user)
        ).select_related(
            "sender", "receiver", "sender__user", "receiver__user"
        )
        return {
            **super().get_context_data(**kwargs),
            "receivers": {ep.receiver.user for ep in queryset},
            "senders": {ep.sender.user for ep in queryset},
            "statuses": STATUS_CHOICES,
        }


class AcceptProposalView(LoginRequiredMixin, View):
    def post(self, request, pk) -> HttpResponseRedirect:
        proposal = get_object_or_404(ExchangeProposal, pk=pk)
        if proposal.receiver.user != request.user:
            raise PermissionDenied("Нельзя принимать чужие предложения.")
        proposal.status = STATUS_CHOICES.ACCEPTED
        proposal.save()
        return redirect("posts:proposals")


class RejectProposalView(LoginRequiredMixin, View):
    def post(self, request, pk) -> HttpResponseRedirect:
        proposal = get_object_or_404(ExchangeProposal, pk=pk)
        if proposal.receiver.user != request.user:
            raise PermissionDenied("Нельзя отклонять чужие предложения.")
        proposal.status = STATUS_CHOICES.REJECTED
        proposal.save()
        return redirect("posts:proposals")


class LogoutRedirectView(LogoutView):
    next_page = "/"
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return self.post(request, *args, **kwargs)
