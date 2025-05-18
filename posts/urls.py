from django.contrib.auth.views import LoginView
from django.urls import path

from posts.views import (
    AcceptProposalView,
    ExchangeProposalCreateView,
    LogoutRedirectView,
    MyPostsListView,
    MyProposalsListView,
    PostCreateView,
    PostDeleteView,
    PostListView,
    PostUpdateView,
    RejectProposalView,
)

app_name = "posts"

urlpatterns = [
    path(
        "",
        PostListView.as_view(),
        name="posts_list",
    ),
    path(
        "create/",
        PostCreateView.as_view(),
        name="create_post",
    ),
    path(
        "my_posts/",
        MyPostsListView.as_view(),
        name="my_posts",
    ),
    path(
        "proposals/",
        MyProposalsListView.as_view(),
        name="proposals",
    ),
    path(
        "proposals/create/",
        ExchangeProposalCreateView.as_view(),
        name="proposal_create",
    ),
    path(
        "proposals/<int:pk>/accept/",
        AcceptProposalView.as_view(),
        name="proposal_accept",
    ),
    path(
        "proposals/<int:pk>/reject/",
        RejectProposalView.as_view(),
        name="proposal_reject",
    ),
    path(
        "my_posts/<int:pk>/delete/",
        PostDeleteView.as_view(),
        name="delete_post",
    ),
    path(
        "my_posts/<int:pk>/",
        PostUpdateView.as_view(),
        name="edit_post",
    ),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html",
            next_page="/",
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutRedirectView.as_view(),
        name="logout",
    ),
]
