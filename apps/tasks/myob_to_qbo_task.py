from apps import celery

from apps.myob import myobreader


# @celery.task()
def read_myob_write_qbo_task(job_id):
    try:

        myobreader.read_data(job_id)
        return True
    except Exception as ex:
        print(ex)
        return False
