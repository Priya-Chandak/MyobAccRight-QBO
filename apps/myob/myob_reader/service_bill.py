import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_service_bill(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        db = get_mongodb_database()
        payload, base_url, headers = get_settings_myob(job_id)

        no_of_records = db["service_bill"].count_documents({'job_id':job_id})

        Collection = db["service_bill"]

        if start_date == "" and end_date == "":
            url = f"{base_url}/Purchase/Bill/Service?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Purchase/Bill/Service?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"

        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {"account": []}

            QuerySet["job_id"] = job_id
            QuerySet["task_id"] = task_id
            QuerySet['table_name'] = "service_bill"
            QuerySet['error'] = None
            QuerySet["is_pushed"] = 0
            QuerySet["UID"] = JsonResponse1[i]["UID"]
            QuerySet["invoice_no"] = JsonResponse1[i]["Number"]
            QuerySet["supplier_invoice_no"] = JsonResponse1[i]["SupplierInvoiceNumber"]
            QuerySet["Subtotal"] = JsonResponse1[i]["Subtotal"]
            QuerySet["TotalTax"] = JsonResponse1[i]["TotalTax"]
            QuerySet["TotalAmount"] = JsonResponse1[i]["TotalAmount"]

            for j in range(0, len(JsonResponse1[i]["Lines"])):
                QuerySet1 = {}
                if JsonResponse1[i]["Lines"][j]["UnitPrice"] == None:
                    QuerySet1["Unit_Price"] = JsonResponse1[i]["Lines"][j]["Total"]
                else:
                    QuerySet1["Unit_Price"] = JsonResponse1[i]["Lines"][j]["UnitPrice"]

                if JsonResponse1[i]["Lines"][j]["UnitCount"] == None:
                    QuerySet1["Quantity"] = 1
                else:
                    QuerySet1["Quantity"] = JsonResponse1[i]["Lines"][j]["UnitCount"]

                if (
                    ("Account" in JsonResponse1[i]["Lines"][j])
                    and (JsonResponse1[i]["Lines"][j]["Account"] is not None)
                    and (JsonResponse1[i]["Lines"][j]["Account"] != {})
                ):
                    QuerySet1["Account_Name"] = JsonResponse1[i]["Lines"][j]["Account"][
                        "Name"
                    ]
                    QuerySet1["DisplayID"] = JsonResponse1[i]["Lines"][j]["Account"][
                        "DisplayID"
                    ]
                QuerySet1["Job"] = JsonResponse1[i]["Lines"][j]["Job"]
                QuerySet1["Discount"] = JsonResponse1[i]["Lines"][j]["DiscountPercent"]
                QuerySet1["Total"] = JsonResponse1[i]["Lines"][j]["Total"]
                QuerySet1["Description"] = JsonResponse1[i]["Lines"][j]["Description"]

                if JsonResponse1[i]["Lines"][j]["TaxCode"] is not None:
                    QuerySet1["Tax_Code"] = JsonResponse1[i]["Lines"][j]["TaxCode"][
                        "Code"
                    ]
                else:
                    QuerySet1["Tax_Code"] = None

                # QuerySet['Total_Amount'] = JsonResponse1[i]['Subtotal']
                QuerySet["account"].append(QuerySet1)

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_service_bill(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
