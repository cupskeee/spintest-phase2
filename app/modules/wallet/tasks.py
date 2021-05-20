from app import app
app.app_context().push()

from rq import get_current_job
from app.models import Tasks

def transfer(wallet, amount):
    wallet.update(balance=wallet.balance+amount)
    wallet["balance"] = wallet.balance+amount
    _set_task_progress(100)

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Tasks.objects(task_id=job.get_id()).first()
        print(task)
        if progress >= 100:
            task.update(complete=True)