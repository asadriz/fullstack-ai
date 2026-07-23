from rest_framework.reverse import reverse

from apps.jobs.tasks import sample_job


class FakeTask:
    id = "sample-task-id"
    status = "PENDING"


class FakeAsyncResult:
    status = "SUCCESS"
    result = {"message": "done"}

    def __init__(self, task_id):
        self.task_id = task_id

    def successful(self):
        return True

    def failed(self):
        return False


def test_trigger_job_returns_task_id(api_client, monkeypatch):
    monkeypatch.setattr(sample_job, "delay", lambda name: FakeTask())

    response = api_client.post(reverse("job-trigger"), {"name": "demo"})

    assert response.status_code == 202
    json_resp = response.json()
    assert json_resp["message"] == "Job queued successfully."
    assert json_resp["data"]["task_id"] == "sample-task-id"
    assert json_resp["data"]["status"] == "PENDING"


def test_job_status_returns_result(api_client, monkeypatch):
    monkeypatch.setattr("apps.jobs.api.views.AsyncResult", FakeAsyncResult)

    response = api_client.get(
        reverse("job-status", kwargs={"task_id": "sample-task-id"})
    )

    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["data"]["task_id"] == "sample-task-id"
    assert json_resp["data"]["status"] == "SUCCESS"
    assert json_resp["data"]["result"] == {"message": "done"}
