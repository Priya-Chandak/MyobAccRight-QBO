import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import get_settings_myob
from apps.util.db_mongo import get_mongodb_database

def get_all_bill(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        dbname = get_mongodb_database()

        payload, base_url, headers = get_settings_myob(job_id)

        no_of_records = dbname["all_bill"].count_documents({'job_id':job_id})

        if (start_date == "" and end_date == "") and (start_date == None and end_date == None):
            url = f"{base_url}/Purchase/Bill?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Purchase/Bill?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"

        Collection = dbname["all_bill"]
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet["job_id"] = job_id
            QuerySet["task_id"] = task_id
            QuerySet['table_name'] = "all_bill"
            QuerySet['error'] = None
            QuerySet["is_pushed"] = 0
            QuerySet["UID"] = JsonResponse1[i]["UID"]
            QuerySet["invoice_no"] = JsonResponse1[i]["Number"]
            QuerySet["supplier_invoice_no"] = JsonResponse1[i]["SupplierInvoiceNumber"]
            QuerySet["Supplier_Name"] = JsonResponse1[i]["Supplier"]["Name"]
            QuerySet["Is_Tax_Inclusive"] = JsonResponse1[i]["IsTaxInclusive"]
            QuerySet["Total_Amount"] = JsonResponse1[i]["TotalAmount"]
            QuerySet["Bill_Date"] = JsonResponse1[i]["Date"]
            QuerySet["Due_Date"] = JsonResponse1[i]["Terms"]["DueDate"]
            QuerySet["Total_Amount"] = JsonResponse1[i]["TotalAmount"]
            QuerySet["Note"] = JsonResponse1[i]["JournalMemo"]

            if JsonResponse1[i]["FreightTaxCode"] is not None:
                QuerySet["Tax_Code"] = JsonResponse1[i]["FreightTaxCode"]["Code"]
            else:
                QuerySet["Tax_Code"] = None

            if JsonResponse1[i]["Category"] is not None:
                QuerySet["Category"] = JsonResponse1[i]["Category"]["Name"]
            else:
                QuerySet["Category"] = None

            arr.append(QuerySet)
        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_all_bill(job_id, task_id)
        else:
            Break

        
    except Exception as ex:
        import traceback
        traceback.print_exc()
        print(ex)
        
