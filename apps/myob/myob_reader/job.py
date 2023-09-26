import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database
from apps.home.data_util import  write_task_execution_step,update_task_execution_status
import sys




def get_myob_job(job_id,task_id):
    try:
        db = get_mongodb_database()
        Collection = db["job"]
        payload, base_url, headers = get_settings_myob(job_id)

        url = f"{base_url}/GeneralLedger/Job"
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 201 or response.status_code == 200 :
            JsonResponse = response.json()
            JsonResponse1 = JsonResponse["Items"]
            if len(JsonResponse1)>0:
                arr = []
                for i in range(0, len(JsonResponse1)):
                    QuerySet = {}
                    QuerySet["job_id"] = job_id
                    QuerySet["task_id"] = task_id
                    QuerySet['table_name'] = "job"
                    QuerySet['error'] = None
                    QuerySet["is_pushed"] = 0
                    QuerySet["UID"] = JsonResponse1[i]["UID"]
                    QuerySet["Number"] = JsonResponse1[i]["Number"]
                    QuerySet["Name"] = JsonResponse1[i]["Name"]
                    QuerySet["Description"] = JsonResponse1[i]["Description"]

                    arr.append(QuerySet)

                if len(arr)>0:
                    Collection.insert_many(arr)

                if JsonResponse["NextPageLink"] is not None:
                    get_myob_job(job_id, task_id)

                else:
                    Break

                
                

    except Exception as ex:
        import traceback
        traceback.print_exc()
        print(ex)

        
