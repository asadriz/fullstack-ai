from celery.result import AsyncResult
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.jobs.api.serializers import JobTriggerSerializer
from apps.jobs.tasks import sample_job
from utils.response.resp import APIResponse


class JobTriggerAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=JobTriggerSerializer, tags=["jobs"])
    def post(self, request):
        serializer = JobTriggerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = sample_job.delay(serializer.validated_data["name"])
        return Response(
            APIResponse.get_response(
                message="Job queued successfully.",
                data={
                    "task_id": task.id,
                    "status": task.status,
                },
            ),
            status=status.HTTP_202_ACCEPTED,
        )


class JobStatusAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(tags=["jobs"])
    def get(self, request, task_id):
        task = AsyncResult(task_id)
        data = {
            "task_id": task_id,
            "status": task.status,
        }

        if task.successful():
            data["result"] = task.result
        elif task.failed():
            data["error"] = str(task.result)

        return Response(APIResponse.get_response(data=data))
