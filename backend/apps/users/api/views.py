from django.db.models import Q, Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.users.api.serializers import (
    OrganizationCreateUpdateSerializer,
    OrganizationSerializer,
    UserAdminSerializer,
    UserAssignOrganizationSerializer,
    UserCreateUpdateSerializer,
)
from apps.users.models import Organization, User
from utils.response.resp import APIResponse
from utils import swagger_fields

TAG = ["admin"]


class IsStaffUser(permissions.BasePermission):
    """
    Permission for staff users only.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


# ================
# Organizations
# ================


class OrganizationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    permission_classes = [IsStaffUser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrganizationCreateUpdateSerializer
        return OrganizationSerializer

    def get_queryset(self):
        queryset = Organization.objects.all()
        search = self.request.query_params.get("search")
        ordering = self.request.query_params.get("ordering")

        if search:
            queryset = queryset.filter(name__icontains=search)

        if ordering:
            allowed = {
                "name": "name",
                "created_at": "created_at",
                "updated_at": "updated_at",
                "users_count": "users__count",
            }
            raw = ordering.strip()
            desc = raw.startswith("-")
            key = raw[1:] if desc else raw
            mapped = allowed.get(key)
            if mapped:
                if key == "users_count":
                    queryset = queryset.annotate(users__count=Count("users"))
                queryset = queryset.order_by(f"-{mapped}" if desc else mapped)
                return queryset

        return queryset.order_by("-created_at")

    @swagger_auto_schema(
        tags=TAG,
        manual_parameters=[
            swagger_fields.ORG_SEARCH_QUERY_PARAM,
            swagger_fields.ORG_ORDERING_QUERY_PARAM,
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=TAG)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OrganizationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    permission_classes = [IsStaffUser]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return OrganizationCreateUpdateSerializer
        return OrganizationSerializer

    @swagger_auto_schema(tags=TAG)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=TAG)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=TAG)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=TAG)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ================
# Users
# ================


class UserListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsStaffUser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateUpdateSerializer
        return UserAdminSerializer

    def get_queryset(self):
        queryset = User.objects.select_related("organization").all()

        # Filter options
        organization_id = self.request.query_params.get("organization")
        is_staff = self.request.query_params.get("is_staff")
        is_active = self.request.query_params.get("is_active")
        search = self.request.query_params.get("search")
        ordering = self.request.query_params.get("ordering")

        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)

        if is_staff is not None:
            is_staff_bool = is_staff.lower() in ["true", "1"]
            queryset = queryset.filter(is_staff=is_staff_bool)

        if is_active is not None:
            is_active_bool = is_active.lower() in ["true", "1"]
            queryset = queryset.filter(is_active=is_active_bool)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(organization__name__icontains=search)
            )

        if ordering:
            allowed = {
                "name": "name",
                "email": "email",
                "date_joined": "date_joined",
                "last_login": "last_login",
                "is_active": "is_active",
                "is_staff": "is_staff",
            }
            raw = ordering.strip()
            desc = raw.startswith("-")
            key = raw[1:] if desc else raw
            mapped = allowed.get(key)
            if mapped:
                return queryset.order_by(f"-{mapped}" if desc else mapped)

        return queryset.order_by("-date_joined")

    @swagger_auto_schema(
        tags=TAG,
        manual_parameters=[
            swagger_fields.USER_ORGANIZATION_QUERY_PARAM,
            swagger_fields.USER_IS_STAFF_QUERY_PARAM,
            swagger_fields.USER_IS_ACTIVE_QUERY_PARAM,
            swagger_fields.USER_SEARCH_QUERY_PARAM,
            swagger_fields.USER_ORDERING_QUERY_PARAM,
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=TAG)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.select_related("organization").all()
    permission_classes = [IsStaffUser]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserCreateUpdateSerializer
        return UserAdminSerializer

    @swagger_auto_schema(tags=TAG)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=TAG)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=TAG)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=TAG)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ================
# User-Organization Assignment
# ================


@swagger_auto_schema(
    method="post",
    tags=TAG,
    request_body=UserAssignOrganizationSerializer,
    responses={
        200: openapi.Response("Success", UserAdminSerializer),
        400: openapi.Response("Bad Request"),
        404: openapi.Response("Not Found"),
    },
)
@api_view(["POST"])
@permission_classes([IsStaffUser])
def assign_user_to_organization(request):
    """
    Assign or unassign a user to/from an organization.
    Set organization_id to null to unassign.
    """
    serializer = UserAssignOrganizationSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data["user_id"]
        organization_id = serializer.validated_data["organization_id"]

        try:
            user = User.objects.get(id=user_id)
            user.organization_id = organization_id
            user.save()

            response_serializer = UserAdminSerializer(user)
            return Response(
                APIResponse.get_response(
                    data=response_serializer.data,
                    message="User organization assignment updated successfully",
                )
            )
        except User.DoesNotExist:
            return Response(
                APIResponse.get_response(error="User not found", code=404),
                status=status.HTTP_404_NOT_FOUND,
            )

    return Response(
        APIResponse.get_response(error=serializer.errors, code=400),
        status=status.HTTP_400_BAD_REQUEST,
    )
