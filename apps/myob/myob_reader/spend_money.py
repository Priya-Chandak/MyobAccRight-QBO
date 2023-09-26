import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_spend_money(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        db = get_mongodb_database()
        Collection = db["myob_spend_money"]

        no_of_records = db["myob_spend_money"].count_documents({'job_id':job_id})
        payload, base_url, headers = get_settings_myob(job_id)

        if start_date == "" and end_date == "":
            url = f"{base_url}/Banking/SpendMoneyTxn?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Banking/SpendMoneyTxn?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"

        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse1 = response.json()
        JsonResponse = JsonResponse1["Items"]

        arr = []
        for i in range(0, len(JsonResponse)):
            QuerySet = {"Lines": []}
            QuerySet["job_id"] = job_id
            QuerySet["task_id"] = task_id
            QuerySet['table_name'] = "myob_spend_money"
            QuerySet['error'] = None
            QuerySet["is_pushed"] = 0
            QuerySet["pay_from"] = JsonResponse[i]["Account"]["Name"]
            QuerySet["payment_no"] = JsonResponse[i]["PaymentNumber"]
            QuerySet["date"] = JsonResponse[i]["Date"]
            QuerySet["memo"] = JsonResponse[i]["Memo"]
            QuerySet["IsTaxInclusive"] = JsonResponse[i]["IsTaxInclusive"]
            QuerySet["Total_Amount"] = JsonResponse[i]["AmountPaid"]
            QuerySet["Total_Tax"] = JsonResponse[i]["TotalTax"]
            QuerySet["Cheque_Printed"] = JsonResponse[i]["ChequePrinted"]
            QuerySet["UID"] = JsonResponse[i]["UID"]

            if JsonResponse[i]["Contact"] is not None:
                QuerySet["contact_type"] = JsonResponse[i]["Contact"]["Type"]
                QuerySet["contact_name"] = JsonResponse[i]["Contact"]["Name"]
            else:
                QuerySet["contact_type"] = None
                QuerySet["contact_name"] = None

            # QuerySet['contact']=QuerySet1
            for j in range(0, len(JsonResponse[i]["Lines"])):
                QuerySet1 = {}
                QuerySet2 = {}

                if JsonResponse[i]["Lines"][j]["Account"] is not None:
                    QuerySet2["account_name"] = JsonResponse[i]["Lines"][j]["Account"][
                        "Name"
                    ]
                    QuerySet2["DisplayID"] = JsonResponse[i]["Lines"][j]["Account"][
                        "DisplayID"
                    ]
                else:
                    QuerySet2["account_name"] = None
                    QuerySet2["DisplayID"] = None

                if JsonResponse[i]["Lines"][j]["TaxCode"] is not None:
                    QuerySet2["taxcode"] = JsonResponse[i]["Lines"][j]["TaxCode"][
                        "Code"
                    ]
                    QuerySet2["tax_id"] = JsonResponse[i]["Lines"][j]["TaxCode"]["UID"]
                else:
                    QuerySet2["taxcode"] = None
                    QuerySet2["tax_id"] = None

                if JsonResponse[i]["Lines"][j]["Job"] is not None:
                    QuerySet2["job"] = JsonResponse[i]["Lines"][j]["Job"]["Name"]
                else:
                    QuerySet2["job"] = None

                QuerySet2["memo"] = JsonResponse[i]["Lines"][j]["Memo"]
                QuerySet2["line_amount"] = JsonResponse[i]["Lines"][j]["Amount"]

                QuerySet["Lines"].append(QuerySet2)

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse1["NextPageLink"] is not None:
            get_spend_money(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
