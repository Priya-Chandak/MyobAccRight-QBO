import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_all_invoice(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        dbname = get_mongodb_database()
        Collection = dbname["all_invoice"]

        payload, base_url, headers = get_settings_myob(job_id)

        no_of_records = dbname["all_invoice"].count_documents({'job_id':job_id})
        
        if start_date == "" and end_date == "":
            url = f"{base_url}/Sale/Invoice?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Sale/Invoice?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet["job_id"] = job_id
            QuerySet["task_id"] = task_id
            QuerySet['table_name'] = "all_invoice"
            QuerySet['error'] = None
            QuerySet["is_pushed"] = 0
            QuerySet["UID"] = JsonResponse1[i]["UID"]
            QuerySet["TotalAmount"] = JsonResponse1[i]["TotalAmount"]
            QuerySet["Customer_Name"] = JsonResponse1[i]["Customer"]["Name"]
            QuerySet["Invoice_Number"] = JsonResponse1[i]["Number"]
            QuerySet["Date"] = JsonResponse1[i]["Date"]
            QuerySet["Due_Date"] = JsonResponse1[i]["Terms"]["DueDate"]
            QuerySet["Is_Tax_Inclusive"] = JsonResponse1[i]["IsTaxInclusive"]
            QuerySet["Customer_Name"] = JsonResponse1[i]["Customer"]["Name"]
            QuerySet["Customer_ID"] = JsonResponse1[i]["Customer"]["UID"]
            QuerySet["Description"] = JsonResponse1[i]["JournalMemo"]
            QuerySet["Comment"] = JsonResponse1[i]["Comment"]
            QuerySet["Customer_po_number"] = JsonResponse1[i]["CustomerPurchaseOrderNumber"]
            QuerySet["Invoice_Type"] = JsonResponse1[i]["InvoiceType"]

            if JsonResponse1[i]["FreightTaxCode"] is not None:
                QuerySet["Tax_Code"] = JsonResponse1[i]["FreightTaxCode"]["Code"]
            else:
                QuerySet["Tax_Code"] = None

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            nextpagelink = JsonResponse["NextPageLink"]
            get_all_invoice(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
