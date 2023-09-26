import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_received_money(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        db = get_mongodb_database()
        Collection = db["received_money"]

        no_of_records = db["received_money"].count_documents({'job_id':job_id})

        payload, base_url, headers = get_settings_myob(job_id)

        if start_date == "" and end_date == "":
            url = f"{base_url}/Banking/ReceiveMoneyTxn?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Banking/ReceiveMoneyTxn?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"

        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {"Line": []}
            QuerySet["job_id"] = job_id
            QuerySet["task_id"] = task_id
            QuerySet['table_name'] = "received_money"
            QuerySet['error'] = None
            QuerySet['UID'] = JsonResponse1[i]["UID"]
            QuerySet["is_pushed"] = 0
            QuerySet["main_account"] = JsonResponse1[i]["Account"]["Name"]
            QuerySet["notes"] = JsonResponse1[i]["Memo"]
            QuerySet["date"] = JsonResponse1[i]["Date"]
            QuerySet["ref_no"] = JsonResponse1[i]["ReceiptNumber"]
            QuerySet["total_tax"] = JsonResponse1[i]["TotalTax"]
            QuerySet["is_tax_inclusive"] = JsonResponse1[i]["IsTaxInclusive"]
            QuerySet["total_amount"] = JsonResponse1[i]["AmountReceived"]
            QuerySet["payment_method"] = JsonResponse1[i]["PaymentMethod"]

            if JsonResponse1[i]["Contact"] is not None:
                QuerySet["contact_type"] = JsonResponse1[i]["Contact"]["Type"]
                QuerySet["contact_name"] = JsonResponse1[i]["Contact"]["Name"]
            else:
                QuerySet["contact_type"] = None
                QuerySet["contact_name"] = None

            for j in range(0, len(JsonResponse1[i]["Lines"])):
                QuerySet2 = {}
                QuerySet2["line_account"] = JsonResponse1[i]["Lines"][j]["Account"][
                    "Name"
                ]
                QuerySet2["account_id"] = JsonResponse1[i]["Lines"][j]["Account"][
                    "DisplayID"
                ]
                QuerySet2["tax_code"] = JsonResponse1[i]["Lines"][j]["TaxCode"]["Code"]
                QuerySet2["line_amount"] = JsonResponse1[i]["Lines"][j]["Amount"]
                QuerySet2["memo"] = JsonResponse1[i]["Lines"][j]["Memo"]

                if JsonResponse1[i]["Lines"][j]["Job"] is not None:
                    QuerySet2["job"] = JsonResponse1[i]["Lines"][j]["Job"]["Name"]
                else:
                    QuerySet2["job"] = None

                QuerySet["Line"].append(QuerySet2)

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_received_money(job_id, task_id)
        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
