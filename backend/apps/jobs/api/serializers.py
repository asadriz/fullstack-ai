from rest_framework import serializers


class JobTriggerSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, default="template", max_length=100)
