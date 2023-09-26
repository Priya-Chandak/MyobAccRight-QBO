import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_myob_class(job_id):
    try:
        dbname = get_mongodb_database()
        Collection = dbname["myob_class"]
        no_of_records = dbname["myob_class"].count_documents({})
        payload, base_url, headers = get_settings_myob(job_id)
        url = f"{base_url}/GeneralLedger/Account?$top=1000&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet["job_id"] = job_id
            QuerySet["Number"] = JsonResponse1[i]["Number"]
            QuerySet["UID"] = JsonResponse1[i]["UID"]
            QuerySet["Name"] = JsonResponse1[i]["Name"]

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            url = JsonResponse["NextPageLink"]
            get_myob_class(job_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
