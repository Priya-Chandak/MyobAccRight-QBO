import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_bank_transfer(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        dbname = get_mongodb_database()
        payload, base_url, headers = get_settings_myob(job_id)

        Collection = dbname["bank_transfer"]
        no_of_records = dbname["bank_transfer"].count_documents({})
        if start_date == "" and end_date == "":
            url = f"{base_url}/Banking/TransferMoneyTxn?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Banking/TransferMoneyTxn?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet["job_id"] = job_id
            QuerySet["task_id"] = task_id
            QuerySet['table_name'] = "bank_transfer"
            QuerySet['error'] = None
            QuerySet["is_pushed"] = 0
            QuerySet["UID"] = JsonResponse1[i]["UID"]

            QuerySet["FromAccountName"] = JsonResponse1[i]["FromAccount"]["Name"]
            QuerySet["FromAccountID"] = JsonResponse1[i]["FromAccount"]["DisplayID"]
            QuerySet["ToAccountName"] = JsonResponse1[i]["ToAccount"]["Name"]
            QuerySet["ToAccountID"] = JsonResponse1[i]["ToAccount"]["DisplayID"]
            QuerySet["TransferNumber"] = JsonResponse1[i]["TransferNumber"]
            QuerySet["Date"] = JsonResponse1[i]["Date"]
            QuerySet["Amount"] = JsonResponse1[i]["Amount"]
            QuerySet["Memo"] = JsonResponse1[i]["Memo"]

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_bank_transfer(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
