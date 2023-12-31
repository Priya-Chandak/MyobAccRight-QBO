import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_trial_balance(job_id):
    try:
        db = get_mongodb_database()
        Collection = db["trial_balance"]

        no_of_records = db["trial_balance"].count_documents({})
        payload, base_url, headers = get_settings_myob(job_id)
        url = f"{base_url}/GeneralLedger/Account?$top=1000&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet["Job_ID"] = job_id
            QuerySet["Account_Name"] = JsonResponse1[i]["Name"]

            if JsonResponse1[i]["CurrentBalance"] < 0:
                QuerySet["Credit"] = JsonResponse1[i]["CurrentBalance"]
            else:
                QuerySet["Debit"] = JsonResponse1[i]["CurrentBalance"]

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_trial_balance(job_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
