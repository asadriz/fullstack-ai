from django.urls import path

from apps.users.api.views import (
    OrganizationDetailAPIView,
    OrganizationListCreateAPIView,
    UserDetailAPIView,
    UserListCreateAPIView,
    assign_user_to_organization,
)

urlpatterns = [
    # Organizations
    path(
        "organizations/",
        OrganizationListCreateAPIView.as_view(),
        name="admin-organizations-list-create",
    ),
    path(
        "organizations/<int:pk>/",
        OrganizationDetailAPIView.as_view(),
        name="admin-organizations-detail",
    ),
    # Users
    path("users/", UserListCreateAPIView.as_view(), name="admin-users-list-create"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="admin-users-detail"),
    path(
        "users/assign-organization/",
        assign_user_to_organization,
        name="admin-users-assign-organization",
    ),
]
