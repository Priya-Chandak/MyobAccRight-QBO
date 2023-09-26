import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import get_settings_myob
from apps.util.db_mongo import get_mongodb_database


def get_accountright_currency(job_id):
    try:
        db = get_mongodb_database()
        Collection = db["accountright_currency"]

        payload, base_url, headers = get_settings_myob(job_id)
        no_of_records = db["accountright_currency"].count_documents({})
        url = f"{base_url}/GeneralLedger/Currency?$top=100&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet['job_id']=job_id
            QuerySet = JsonResponse["Items"][i]
            arr.append(QuerySet)

        if isinstance(arr, list):
            Collection.insert_many(arr)

        else:
            Collection.insert_one(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_accountright_currency(job_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
