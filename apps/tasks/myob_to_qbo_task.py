from apps.myob import myobreader

def read_myob_write_qbo_task(job_id):
    try:
        myobreader.read_data(job_id)
        return True
    except Exception as ex:
        print(ex)
        return False
