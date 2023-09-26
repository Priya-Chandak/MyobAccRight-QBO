import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.home.data_util import get_job_details
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_miscellaneous_bill(job_id, task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        db = get_mongodb_database()
        payload, base_url, headers = get_settings_myob(job_id)
        no_of_records = db["misc_bill"].count_documents({})
        Collection = db["misc_bill"]

        if start_date == "" and end_date == "":
            url = f"{base_url}/Purchase/Bill/Miscellaneous?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Purchase/Bill/Miscellaneous?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"

        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet1 = {"account": []}
            QuerySet1["job_id"] = job_id
            QuerySet1["task_id"] =task_id
            QuerySet1["table_name"] ="misc_bill"
            QuerySet1["error"] = None
            QuerySet1["is_pushed"] = 0
                
            QuerySet1["invoice_no"] = JsonResponse1[i]["Number"]
            QuerySet1["supplier_invoice_no"] = JsonResponse1[i]["SupplierInvoiceNumber"]
            QuerySet1["UID"] = JsonResponse1[i]["UID"]
            for j in range(0, len(JsonResponse1[i]["Lines"])):
                QuerySet2 = {}
                QuerySet2["Acc_name"] = JsonResponse1[i]["Lines"][j]["account"]["Name"]
                QuerySet2["DisplayID"] = JsonResponse1[i]["Lines"][j]["account"][
                    "DisplayID"
                ]

                QuerySet2["Type"] = JsonResponse1[i]["Lines"][j]["Type"]
                QuerySet2["Description"] = JsonResponse1[i]["Lines"][j]["Description"]
                QuerySet2["Total"] = JsonResponse1[i]["Lines"][j]["Total"]

                if JsonResponse1[i]["Lines"][j]["Job"] is not None:
                    QuerySet2["Job"] = JsonResponse1[i]["Lines"][j]["Job"]
                else:
                    QuerySet2["Job"] = None

                if JsonResponse1[i]["Lines"][j]["TaxCode"] is not None:
                    QuerySet2["Tax_Code"] = JsonResponse1[i]["Lines"][j]["TaxCode"][
                        "Code"
                    ]
                else:
                    QuerySet2["Tax_Code"] = None

                QuerySet1["account"].append(QuerySet2)

            arr.append(QuerySet1)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_miscellaneous_bill(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
