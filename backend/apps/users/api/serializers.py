from rest_framework import serializers

from apps.users.models import Organization, User


class OrganizationSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ["id", "name", "created_at", "updated_at", "users_count"]

    def get_users_count(self, obj):
        return obj.users.count()


class OrganizationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name"]


class UserAdminSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(
        source="organization.name", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "organization",
            "organization_name",
            "date_joined",
            "last_login",
        ]


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["name", "email", "password", "organization", "is_active", "is_staff"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            # Set a default password or generate one
            user.set_password("changeme123")
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserAssignOrganizationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    organization_id = serializers.IntegerField(allow_null=True)

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value

    def validate_organization_id(self, value):
        if value is not None and not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Organization does not exist")
        return value
