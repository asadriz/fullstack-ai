from django.urls import path

from apps.jobs.api.views import JobStatusAPIView, JobTriggerAPIView

urlpatterns = [
    path("trigger/", JobTriggerAPIView.as_view(), name="job-trigger"),
    path("<str:task_id>/", JobStatusAPIView.as_view(), name="job-status"),
]
