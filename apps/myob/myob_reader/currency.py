import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_currency(job_id):
    try:
        db = get_mongodb_database()
        Collection = db["currency"]
        payload, base_url, headers = get_settings_myob(job_id)

        no_of_records = db["currency"].count_documents({})
        url = f"{base_url}/GeneralLedger/Currency?$top=100&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet["job_id"] = job_id
            QuerySet["Deposit_Into"] = JsonResponse1[i]["UID"]
            QuerySet["Notes"] = JsonResponse1[i]["Code"]
            QuerySet["Date"] = JsonResponse1[i]["CurrencyName"]
            QuerySet["Reference_No"] = JsonResponse1[i]["CurrencyRate"]
            arr.append(QuerySet)

        if isinstance(arr, list):
            Collection.insert_many(arr)

        else:
            Collection.insert_one(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_currency(job_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
