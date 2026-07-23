from celery import shared_task


@shared_task(bind=True)
def sample_job(self, name="template"):
    return {
        "task_id": self.request.id,
        "message": f"Sample job completed for {name}.",
    }
