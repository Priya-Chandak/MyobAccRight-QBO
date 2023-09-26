import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.home.data_util import get_job_details
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_item_invoice(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        payload, base_url, headers = get_settings_myob(job_id)
        db = get_mongodb_database()
        Collection = db["item_invoice"]
        no_of_records = db["item_invoice"].count_documents({"job_id":job_id})

        if start_date == "" and end_date == "":
            url = f"{base_url}/Sale/Invoice/Item?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Sale/Invoice/Item?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"

        print(url)
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []

        for i in range(0, len(JsonResponse1)):
            QuerySet1 = {"Item": []}
            QuerySet1["job_id"] = job_id
            QuerySet1["task_id"] = task_id
            QuerySet1['table_name'] = "item_invoice"
            QuerySet1['error'] = None
            QuerySet1["is_pushed"] = 0
            QuerySet1["UID"] = JsonResponse1[i]["UID"]
            QuerySet1["invoice_no"] = JsonResponse1[i]["Number"]
            QuerySet1["customer_purchase_order_no"] = JsonResponse1[i][
                "CustomerPurchaseOrderNumber"
            ]
            QuerySet1["IsTaxInclusive"] = JsonResponse1[i]["IsTaxInclusive"]
            QuerySet1["Subtotal"] = JsonResponse1[i]["Subtotal"]
            QuerySet1["TotalTax"] = JsonResponse1[i]["TotalTax"]
            QuerySet1["TotalAmount"] = JsonResponse1[i]["TotalAmount"]
            QuerySet1["JournalMemo"] = JsonResponse1[i]["JournalMemo"]

            for j in range(0, len(JsonResponse1[i]["Lines"])):
                QuerySet2 = {}

                if "Item" in JsonResponse1[i]["Lines"][j]:
                    if JsonResponse1[i]["Lines"][j]["Item"] is not None:
                        if "Name" in JsonResponse1[i]["Lines"][j]["Item"]:
                            QuerySet2["item_name"] = JsonResponse1[i]["Lines"][j][
                                "Item"
                            ]["Name"]
                        if "UID" in JsonResponse1[i]["Lines"][j]["Item"]:
                            QuerySet2["item_id"] = JsonResponse1[i]["Lines"][j]["Item"][
                                "UID"
                            ]
                        if "Number" in JsonResponse1[i]["Lines"][j]["Item"]:
                            QuerySet2["item_value"] = JsonResponse1[i]["Lines"][j][
                                "Item"
                            ]["Number"]

                if JsonResponse1[i]["Comment"] is not None:
                    QuerySet2["comment"] = JsonResponse1[i]["Comment"]
                else:
                    QuerySet2["comment"] = None

                if len(JsonResponse1[i]["Lines"]) != 0:
                    # if 'ShipQuantity' in JsonResponse1[i]['Lines'][j]:
                    #     QuerySet2['ship_quantity'] = JsonResponse1[i]['Lines'][j]['ShipQuantity']
                    # else:
                    #     QuerySet2['ship_quantity'] = 0

                    # if JsonResponse1[i]['Lines'][j]['UnitCount'] is not None:
                    #     QuerySet2['unit_count'] = JsonResponse1[i]['Lines'][j]['UnitCount']
                    # else:
                    #     QuerySet2['unit_count'] = 0

                    if "ShipQuantity" in JsonResponse1[i]["Lines"][j]:
                        if (JsonResponse1[i]["Lines"][j]["ShipQuantity"] != 0) and (
                            JsonResponse1[i]["Lines"][j]["ShipQuantity"] is not None
                        ):
                            QuerySet2["ship_quantity"] = JsonResponse1[i]["Lines"][j][
                                "ShipQuantity"
                            ]
                    if "UnitCount" in JsonResponse1[i]["Lines"][j]:
                        if (JsonResponse1[i]["Lines"][j]["UnitCount"] != 0) and (
                            JsonResponse1[i]["Lines"][j]["UnitCount"] is not None
                        ):
                            QuerySet2["ship_quantity"] = JsonResponse1[i]["Lines"][j][
                                "UnitCount"
                            ]
                    if (
                        JsonResponse1[i]["Lines"][j]["UnitCount"] == 0
                        and JsonResponse1[i]["Lines"][j]["ShipQuantity"] == 0
                    ):
                        QuerySet2["ship_quantity"] = 0

                    if "UnitPrice" in JsonResponse1[i]["Lines"][j]:
                        QuerySet2["unit_price"] = JsonResponse1[i]["Lines"][j][
                            "UnitPrice"
                        ]
                    if "DiscountPercent" in JsonResponse1[i]["Lines"][j]:
                        QuerySet2["discount"] = JsonResponse1[i]["Lines"][j][
                            "DiscountPercent"
                        ]
                    if "Total" in JsonResponse1[i]["Lines"][j]:
                        QuerySet2["amount"] = JsonResponse1[i]["Lines"][j]["Total"]
                    if JsonResponse1[i]["Lines"][j]["Description"] is not None:
                        QuerySet2["description"] = JsonResponse1[i]["Lines"][j][
                            "Description"
                        ]
                    else:
                        QuerySet2["description"] = None

                    if "TaxCode" in JsonResponse1[i]["Lines"][j]:
                        if JsonResponse1[i]["Lines"][j]["TaxCode"] is not None:
                            QuerySet2["taxcode"] = JsonResponse1[i]["Lines"][j][
                                "TaxCode"
                            ]["Code"]
                        else:
                            QuerySet2["taxcode"] = None

                    if "Job" in JsonResponse1[i]["Lines"][j]:
                        if JsonResponse1[i]["Lines"][j]["Job"] is not None:
                            QuerySet2["job"] = JsonResponse1[i]["Lines"][j]["Job"]
                        else:
                            QuerySet2["job"] = None

                    if 'Account' in JsonResponse1[i]["Lines"][j]: 
                        if JsonResponse1[i]["Lines"][j]["Account"] is not None:
                            QuerySet2["account_name"] = JsonResponse1[i]["Lines"][j]["Account"]["Name"]
                            QuerySet2["account_id"] = JsonResponse1[i]["Lines"][j][
                                "Account"
                            ]["UID"]
                            QuerySet2["DisplayID"] = JsonResponse1[i]["Lines"][j][
                                "Account"
                            ]["DisplayID"]

                if JsonResponse1[i]["Customer"] is not None:
                    QuerySet1["customer_name"] = JsonResponse1[i]["Customer"]["Name"]
                    if "DisplayID" in JsonResponse1[i]["Customer"]:
                        QuerySet1["customer_id"] = JsonResponse1[i]["Customer"][
                            "DisplayID"
                        ]
                else:
                    QuerySet1["customer_name"] = None
                    QuerySet1["customer_id"] = None
                QuerySet1["invoice_date"] = JsonResponse1[i]["Date"]
                QuerySet1["due_date"] = JsonResponse1[i]["Terms"]["DueDate"]
                QuerySet1["Item"].append(QuerySet2)

            arr.append(QuerySet1)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_item_invoice(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        


def get_classified_invoice(job_id,task_id):
    try:
        db = get_mongodb_database()
        single_item_invoice = db["single_item_invoice"]
        multiple_item_invoice = db["multiple_item_invoice"]

        item_invoice1 = db["item_invoice"].find({"job_id": job_id})
        Q1 = []

        for i in item_invoice1:
            Q1.append(i)

        single = []
        multiple = []

        for p1 in range(0, len(Q1)):
            if len(Q1[p1]["Item"]) == 1:
                single.append(Q1[p1])
            elif len(Q1[p1]["Item"]) > 1:
                multiple.append(Q1[p1])
            else:
                pass

        if len(single) > 0:
            single_item_invoice.insert_many(single)
        if len(multiple) > 0:
            multiple_item_invoice.insert_many(multiple)

    except Exception as ex:
        traceback.print_exc()
        
