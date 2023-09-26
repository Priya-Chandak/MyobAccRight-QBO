import traceback
from ast import Break

import requests
import sys

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database
from apps.home.data_util import  write_task_execution_step,update_task_execution_status



def get_taxcode_myob(job_id, task_id):
    try:
        db = get_mongodb_database()
        Collection1 = db["taxcode_myob"]
        no_of_records = db["taxcode"].count_documents({'job_id':job_id})
        payload, base_url, headers = get_settings_myob(job_id)
        url = f"{base_url}/GeneralLedger/TaxCode?$top=1000&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {"job_id": job_id, "task_id": task_id, "is_pushed": 0, "table_name": "taxcode_myob", }
            QuerySet["UID"] = JsonResponse1[i]["UID"]
            QuerySet["Code"] = JsonResponse1[i]["Code"]
            QuerySet["Rate"] = JsonResponse1[i]["Rate"]

            arr.append(QuerySet)

        Collection1.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            url = JsonResponse["NextPageLink"]
            get_taxcode_myob(job_id)

        else:
            Break

        step_name = "Reading data from tax code"
        write_task_execution_step(task_id, status=1, step=step_name)

    except Exception as ex:
        step_name = "Access token not valid"
        write_task_execution_step(task_id, status=0, step=step_name)
        update_task_execution_status( task_id, status=0, task_type="write")
        import traceback
        traceback.print_exc()
        print(ex)
        sys.exit(0)
        
