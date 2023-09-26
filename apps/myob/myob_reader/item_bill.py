import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.home.data_util import get_job_details
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_item_bill(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        db = get_mongodb_database()
        payload, base_url, headers = get_settings_myob(job_id)
        no_of_records = db["item_bill"].count_documents({'job_id':job_id})
        Collection = db["item_bill"]

        if start_date == "" and end_date == "":
            url = f"{base_url}/Purchase/Bill/Item?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Purchase/Bill/Item?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"

        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {
                "account": [],
                "job_id": job_id,
                "task_id" :task_id,
                "table_name":"item_bill",
                "error":None,
                "is_pushed":0,
                "UID": JsonResponse1[i]["UID"],
                "Comment": JsonResponse1[i]["Comment"],
                "invoice_no": JsonResponse1[i]["Number"],
                "supplier_invoice_no": JsonResponse1[i]["SupplierInvoiceNumber"],
                "JournalMemo": JsonResponse1[i]["JournalMemo"],
                "Subtotal": JsonResponse1[i]["Subtotal"],
                "TotalTax": JsonResponse1[i]["TotalTax"],
                "TotalAmount": JsonResponse1[i]["TotalAmount"],
                "IsTaxInclusive": JsonResponse1[i]["IsTaxInclusive"],
            }

            if JsonResponse1[i]["Lines"] is not None:
                for j in range(0, len(JsonResponse1[i]["Lines"])):
                    QuerySet1 = {}
                    if JsonResponse1[i]["Lines"][j]["Item"] is not None:
                        QuerySet1["Item_name"] = JsonResponse1[i]["Lines"][j]["Item"][
                            "Name"
                        ]
                    QuerySet1["Account_Name"] = JsonResponse1[i]["Lines"][j]["Account"][
                        "Name"
                    ]
                    QuerySet1["DisplayID"] = JsonResponse1[i]["Lines"][j]["Account"][
                        "DisplayID"
                    ]

                    QuerySet1["Unit_Price"] = JsonResponse1[i]["Lines"][j]["UnitPrice"]
                    QuerySet1["Total"] = JsonResponse1[i]["Lines"][j]["Total"]
                    QuerySet1["Quantity"] = JsonResponse1[i]["Lines"][j]["BillQuantity"]
                    QuerySet1["Description"] = JsonResponse1[i]["Lines"][j][
                        "Description"
                    ]
                    if "DiscountPercent" in JsonResponse1[i]["Lines"][j]:
                        QuerySet1["Discount"] = JsonResponse1[i]["Lines"][j][
                            "DiscountPercent"
                        ]
                    else:
                        QuerySet1["Discount"] = 0

                    if JsonResponse1[i]["Lines"][j]["Job"] is not None:
                        QuerySet1["Job"] = JsonResponse1[i]["Lines"][j]["Job"]
                    else:
                        QuerySet1["Job"] = None

                    if JsonResponse["Items"][i]["Lines"][j]["TaxCode"] is not None:
                        QuerySet1["Tax_Code"] = JsonResponse1[i]["Lines"][j]["TaxCode"][
                            "Code"
                        ]
                    else:
                        QuerySet1["Tax_Code"] = None

                    QuerySet["account"].append(QuerySet1)

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_item_bill(job_id, task_id)

        else:
            Break
    except Exception as ex:
        traceback.print_exc()
        
