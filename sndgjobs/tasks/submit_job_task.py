from ..models.SNDGJob import SNDGJob, SNDGJobStatus
from celery import shared_task
import traceback


@shared_task
def submit_job_task(job_id :int):
    job = SNDGJob.objects.get(id=job_id)
    job.init()
    job.save()
    try:
        job.run()
        job.update_status(SNDGJobStatus.FINISHED)
        job.save()
    except Exception:
        job.update_status(SNDGJobStatus.ERROR,traceback.format_exc())
        job.save()
