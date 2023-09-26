import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_taxcode(job_id,task_id):
    try:
        db = get_mongodb_database()
        Collection = db["taxcode_myob"]
        no_of_records = db["taxcode_myob"].count_documents({"job_id":job_id})
        payload, base_url, headers = get_settings_myob(job_id)

        url = f"{base_url}/GeneralLedger/TaxCode?$top=1000&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]
        
        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet["job_id"] = job_id
            QuerySet["task_id"] = task_id
            QuerySet['table_name'] = "taxcode"
            QuerySet['error'] = None
            QuerySet["is_pushed"] = 0
            QuerySet["UID"] = JsonResponse1[i]["UID"]
            QuerySet["Code"] = JsonResponse1[i]["Code"]
            QuerySet["Rate"] = JsonResponse1[i]["Rate"]
            QuerySet["Type"] = JsonResponse1[i]["Type"]
            QuerySet["Description"] = JsonResponse1[i]["Description"]

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            url = JsonResponse["NextPageLink"]
            get_taxcode(job_id,task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
