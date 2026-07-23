from drf_yasg import openapi

object_id = openapi.Parameter(
    "object_id",
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    required=False,
)

id = openapi.Parameter(
    "id",
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    required=False,
)

file = openapi.Parameter(
    "file",
    openapi.IN_FORM,
    description="file of any type.",
    type=openapi.TYPE_FILE,
    required=True,
)

file_id = openapi.Parameter(
    "file_id",
    openapi.IN_QUERY,
    description="file of any type.",
    type=openapi.TYPE_FILE,
    required=True,
)

ORG_SEARCH_QUERY_PARAM = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="Search organizations by name",
    type=openapi.TYPE_STRING,
    required=False,
)

ORG_ORDERING_QUERY_PARAM = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="Order by name, created_at, updated_at, users_count (prefix with - for desc)",
    type=openapi.TYPE_STRING,
    required=False,
)

USER_ORGANIZATION_QUERY_PARAM = openapi.Parameter(
    "organization",
    openapi.IN_QUERY,
    description="Filter by organization ID",
    type=openapi.TYPE_INTEGER,
    required=False,
)

USER_IS_STAFF_QUERY_PARAM = openapi.Parameter(
    "is_staff",
    openapi.IN_QUERY,
    description="Filter by staff status",
    type=openapi.TYPE_BOOLEAN,
    required=False,
)

USER_IS_ACTIVE_QUERY_PARAM = openapi.Parameter(
    "is_active",
    openapi.IN_QUERY,
    description="Filter by active status",
    type=openapi.TYPE_BOOLEAN,
    required=False,
)

USER_SEARCH_QUERY_PARAM = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="Search by name or email",
    type=openapi.TYPE_STRING,
    required=False,
)

USER_ORDERING_QUERY_PARAM = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="Order by name, email, date_joined, last_login, is_active, is_staff (prefix with - for desc)",
    type=openapi.TYPE_STRING,
    required=False,
)
