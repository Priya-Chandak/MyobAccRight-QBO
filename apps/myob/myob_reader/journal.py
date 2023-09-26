import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.home.data_util import get_job_details
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_journal(job_id,task_id):
   
    try:
        start_date, end_date = get_job_details(job_id)
        db = get_mongodb_database()
        Collection = db["journal"]
        payload, base_url, headers = get_settings_myob(job_id)
        no_of_records = db["journal"].count_documents({})

        if start_date == "" and end_date == "":
            url = f"{base_url}/GeneralLedger/GeneralJournal?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/GeneralLedger/GeneralJournal?$top=1000&$skip={no_of_records}&$filter=DateOccurred ge datetime'{start_date[0:10]}' and DateOccurred le datetime'{end_date[0:10]}'"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {"is_credit_debit": []}
            QuerySet["job_id"] = job_id
            QuerySet["task_id"] = task_id
            QuerySet['table_name'] = "journal"
            QuerySet['error'] = None
            QuerySet["is_pushed"] = 0
            QuerySet["Referrence_No"] = JsonResponse1[i]["DisplayID"]
            QuerySet["Date"] = JsonResponse1[i]["DateOccurred"]
            QuerySet["Memo"] = JsonResponse1[i]["Memo"]
            QuerySet["GSTReportingMethod"] = JsonResponse1[i]["GSTReportingMethod"]
            QuerySet["IsTaxInclusive"] = JsonResponse1[i]["IsTaxInclusive"]
            QuerySet["UID"] = JsonResponse1[i]["UID"]

            for j in range(0, len(JsonResponse1[i]["Lines"])):
                QuerySet1 = {}
                QuerySet1["line_amount"] = JsonResponse1[i]["Lines"][j]["Amount"]
                QuerySet1["IsCredit"] = JsonResponse1[i]["Lines"][j]["IsCredit"]
                QuerySet1["Description"] = JsonResponse1[i]["Lines"][j]["Memo"]
                QuerySet1["Account_Name"] = JsonResponse1[i]["Lines"][j]["Account"]["Name"]
                QuerySet1["DisplayID"] = JsonResponse1[i]["Lines"][j]["Account"][
                    "DisplayID"
                ]
                QuerySet1["Tax_Amount"] = JsonResponse1[i]["Lines"][j]["TaxAmount"]
                QuerySet1["Unit_Count"] = JsonResponse1[i]["Lines"][j]["UnitCount"]

                if JsonResponse1[i]["Lines"][j]["Job"] is not None:
                    QuerySet1["Job"] = JsonResponse1[i]["Lines"][j]["Job"]["Name"]

                if JsonResponse1[i]["Lines"][j]["TaxCode"] is not None:
                    QuerySet1["taxcode"] = JsonResponse1[i]["Lines"][j]["TaxCode"][
                        "Code"
                    ]
                else:
                    QuerySet1["taxcode"] = None

                QuerySet["is_credit_debit"].append(QuerySet1)

            arr.append(QuerySet)
        
        
        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_journal(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
