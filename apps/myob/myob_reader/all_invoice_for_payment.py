import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database
from apps.home.data_util import  write_task_execution_step,update_task_execution_status
import sys



def get_all_invoice_for_payments(job_id,task_id):
    try:

        dbname = get_mongodb_database()
        Collection = dbname["all_invoice"]

        payload, base_url, headers = get_settings_myob(job_id)

        no_of_records = dbname["all_invoice"].count_documents({'job_id':job_id})

        url = f"{base_url}/Sale/Invoice?$top=500&$skip={no_of_records}"
        print(url)
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
            QuerySet["Customer_po_number"]=JsonResponse1[i]["CustomerPurchaseOrderNumber"]
            QuerySet["Invoice_Type"] = JsonResponse1[i]["InvoiceType"]

            if JsonResponse1[i]["FreightTaxCode"] is not None:
                QuerySet["Tax_Code"] = JsonResponse1[i]["FreightTaxCode"]["Code"]
            else:
                QuerySet["Tax_Code"] = None

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            nextpagelink = JsonResponse["NextPageLink"]
            get_all_invoice_for_payments(job_id, task_id)

        else:
            Break

        step_name = "Reading data from all invoice for payment"
        write_task_execution_step(task_id, status=1, step=step_name)
             


    except Exception as ex:
        step_name = "Access token not valid"
        write_task_execution_step(task_id, status=0, step=step_name)
        update_task_execution_status( task_id, status=0, task_type="write")
        import traceback
        traceback.print_exc()
        print(ex)
        sys.exit(0)
        
